"""
人体姿态检测与动作分析模块
"""
import cv2
import mediapipe as mp
import numpy as np
from typing import List, Dict, Tuple, Optional
from loguru import logger
import json
from dataclasses import dataclass
from datetime import datetime


@dataclass
class PoseKeypoint:
    """姿态关键点"""
    x: float
    y: float
    z: float
    visibility: float
    name: str


class PoseDetector:
    """姿态检测器 - 基于MediaPipe"""
    
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=2,
            smooth_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        logger.info("初始化姿态检测器")
    
    def detect_pose(self, image: np.ndarray) -> Optional[List[PoseKeypoint]]:
        """检测图像中的人体姿态"""
        # 转换颜色空间
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # 检测姿态
        results = self.pose.process(image_rgb)
        
        if not results.pose_landmarks:
            return None
        
        # 提取关键点
        keypoints = []
        landmark_names = [
            'NOSE', 'LEFT_EYE_INNER', 'LEFT_EYE', 'LEFT_EYE_OUTER',
            'RIGHT_EYE_INNER', 'RIGHT_EYE', 'RIGHT_EYE_OUTER',
            'LEFT_EAR', 'RIGHT_EAR', 'MOUTH_LEFT', 'MOUTH_RIGHT',
            'LEFT_SHOULDER', 'RIGHT_SHOULDER', 'LEFT_ELBOW', 'RIGHT_ELBOW',
            'LEFT_WRIST', 'RIGHT_WRIST', 'LEFT_PINKY', 'RIGHT_PINKY',
            'LEFT_INDEX', 'RIGHT_INDEX', 'LEFT_THUMB', 'RIGHT_THUMB',
            'LEFT_HIP', 'RIGHT_HIP', 'LEFT_KNEE', 'RIGHT_KNEE',
            'LEFT_ANKLE', 'RIGHT_ANKLE', 'LEFT_HEEL', 'RIGHT_HEEL',
            'LEFT_FOOT_INDEX', 'RIGHT_FOOT_INDEX'
        ]
        
        for idx, landmark in enumerate(results.pose_landmarks.landmark):
            keypoint = PoseKeypoint(
                x=landmark.x,
                y=landmark.y,
                z=landmark.z,
                visibility=landmark.visibility,
                name=landmark_names[idx] if idx < len(landmark_names) else f"POINT_{idx}"
            )
            keypoints.append(keypoint)
        
        return keypoints
    
    def draw_pose(self, image: np.ndarray, keypoints: List[PoseKeypoint]) -> np.ndarray:
        """在图像上绘制姿态"""
        # 这里简化处理，实际应该使用MediaPipe的绘制工具
        annotated_image = image.copy()
        
        for kp in keypoints:
            if kp.visibility > 0.5:
                x = int(kp.x * image.shape[1])
                y = int(kp.y * image.shape[0])
                cv2.circle(annotated_image, (x, y), 5, (0, 255, 0), -1)
        
        return annotated_image
    
    def calculate_angle(self, p1: PoseKeypoint, p2: PoseKeypoint, p3: PoseKeypoint) -> float:
        """计算三个关键点之间的角度"""
        # 向量
        v1 = np.array([p1.x - p2.x, p1.y - p2.y])
        v2 = np.array([p3.x - p2.x, p3.y - p2.y])
        
        # 计算角度
        cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-6)
        angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))
        
        return np.degrees(angle)


class ActionAnalyzer:
    """动作分析器"""
    
    def __init__(self):
        self.detector = PoseDetector()
        logger.info("初始化动作分析器")
    
    def analyze_squat(self, keypoints: List[PoseKeypoint]) -> Dict:
        """分析深蹲动作"""
        # 获取关键点
        left_hip = next((kp for kp in keypoints if kp.name == 'LEFT_HIP'), None)
        left_knee = next((kp for kp in keypoints if kp.name == 'LEFT_KNEE'), None)
        left_ankle = next((kp for kp in keypoints if kp.name == 'LEFT_ANKLE'), None)
        
        if not all([left_hip, left_knee, left_ankle]):
            return {"error": "关键点检测不完整"}
        
        # 计算膝关节角度
        knee_angle = self.detector.calculate_angle(left_hip, left_knee, left_ankle)
        
        # 评估动作
        feedback = []
        score = 100
        
        if knee_angle > 120:
            feedback.append("蹲得不够深，建议膝关节弯曲角度达到90度左右")
            score -= 20
        elif knee_angle < 70:
            feedback.append("蹲得过深，可能对膝关节造成压力")
            score -= 10
        
        # 检查膝盖是否超过脚尖
        if left_knee.x > left_ankle.x + 0.05:
            feedback.append("膝盖超过脚尖，建议调整姿势")
            score -= 15
        
        result = {
            "action": "深蹲",
            "knee_angle": knee_angle,
            "score": max(0, score),
            "feedback": feedback if feedback else ["动作标准"],
            "status": "优秀" if score >= 90 else "良好" if score >= 75 else "需改进"
        }
        
        return result
    
    def analyze_plank(self, keypoints: List[PoseKeypoint]) -> Dict:
        """分析平板支撑动作"""
        shoulder = next((kp for kp in keypoints if kp.name == 'LEFT_SHOULDER'), None)
        hip = next((kp for kp in keypoints if kp.name == 'LEFT_HIP'), None)
        ankle = next((kp for kp in keypoints if kp.name == 'LEFT_ANKLE'), None)
        
        if not all([shoulder, hip, ankle]):
            return {"error": "关键点检测不完整"}
        
        # 计算身体角度
        body_angle = self.detector.calculate_angle(shoulder, hip, ankle)
        
        feedback = []
        score = 100
        
        # 理想的平板支撑应该接近180度
        if abs(body_angle - 180) > 15:
            feedback.append("身体不够平直，注意保持一条直线")
            score -= 20
        
        # 检查臀部高度
        if hip.y < shoulder.y - 0.05:
            feedback.append("臀部抬得过高")
            score -= 15
        elif hip.y > shoulder.y + 0.05:
            feedback.append("臀部下沉，注意收紧核心")
            score -= 15
        
        result = {
            "action": "平板支撑",
            "body_angle": body_angle,
            "score": max(0, score),
            "feedback": feedback if feedback else ["动作标准"],
            "status": "优秀" if score >= 90 else "良好" if score >= 75 else "需改进"
        }
        
        return result
    
    def analyze_push_up(self, keypoints: List[PoseKeypoint]) -> Dict:
        """分析俯卧撑动作"""
        shoulder = next((kp for kp in keypoints if kp.name == 'LEFT_SHOULDER'), None)
        elbow = next((kp for kp in keypoints if kp.name == 'LEFT_ELBOW'), None)
        wrist = next((kp for kp in keypoints if kp.name == 'LEFT_WRIST'), None)
        
        if not all([shoulder, elbow, wrist]):
            return {"error": "关键点检测不完整"}
        
        # 计算肘关节角度
        elbow_angle = self.detector.calculate_angle(shoulder, elbow, wrist)
        
        feedback = []
        score = 100
        
        # 下降阶段肘关节应该在90度左右
        if elbow_angle > 120:
            feedback.append("下降不够，建议肘关节弯曲至90度")
            score -= 20
        elif elbow_angle < 70:
            feedback.append("下降过低，注意保护肩关节")
            score -= 10
        
        result = {
            "action": "俯卧撑",
            "elbow_angle": elbow_angle,
            "score": max(0, score),
            "feedback": feedback if feedback else ["动作标准"],
            "status": "优秀" if score >= 90 else "良好" if score >= 75 else "需改进"
        }
        
        return result


class BVHConverter:
    """BVH格式转换器"""
    
    def __init__(self):
        logger.info("初始化BVH转换器")
    
    def keypoints_to_bvh(self, keypoints_sequence: List[List[PoseKeypoint]], 
                        fps: int = 30) -> str:
        """将关键点序列转换为BVH格式"""
        frame_time = 1.0 / fps
        
        # BVH头部
        bvh_header = """HIERARCHY
ROOT Hips
{
    OFFSET 0.0 0.0 0.0
    CHANNELS 6 Xposition Yposition Zposition Zrotation Xrotation Yrotation
    JOINT Spine
    {
        OFFSET 0.0 10.0 0.0
        CHANNELS 3 Zrotation Xrotation Yrotation
        JOINT Chest
        {
            OFFSET 0.0 10.0 0.0
            CHANNELS 3 Zrotation Xrotation Yrotation
            End Site
            {
                OFFSET 0.0 10.0 0.0
            }
        }
    }
}
"""
        
        # BVH运动数据
        bvh_motion = f"MOTION\nFrames: {len(keypoints_sequence)}\nFrame Time: {frame_time}\n"
        
        for frame_keypoints in keypoints_sequence:
            # 简化处理：提取髋部位置
            hip = next((kp for kp in frame_keypoints if 'HIP' in kp.name), None)
            if hip:
                bvh_motion += f"{hip.x} {hip.y} {hip.z} 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0\n"
        
        return bvh_header + bvh_motion
    
    def save_bvh(self, bvh_data: str, filepath: str):
        """保存BVH文件"""
        with open(filepath, 'w') as f:
            f.write(bvh_data)
        logger.info(f"BVH文件已保存: {filepath}")


class FitnessMotionCapture:
    """健身动作捕捉系统"""
    
    def __init__(self):
        self.analyzer = ActionAnalyzer()
        self.bvh_converter = BVHConverter()
        logger.info("初始化健身动作捕捉系统")
    
    def process_video(self, video_path: str, action_type: str = "squat") -> Dict:
        """处理视频并分析动作"""
        logger.info(f"处理视频: {video_path}")
        
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            return {"error": "无法打开视频文件"}
        
        frame_count = 0
        analysis_results = []
        keypoints_sequence = []
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # 检测姿态
            keypoints = self.analyzer.detector.detect_pose(frame)
            
            if keypoints:
                keypoints_sequence.append(keypoints)
                
                # 分析动作
                if action_type == "squat":
                    result = self.analyzer.analyze_squat(keypoints)
                elif action_type == "plank":
                    result = self.analyzer.analyze_plank(keypoints)
                elif action_type == "push_up":
                    result = self.analyzer.analyze_push_up(keypoints)
                else:
                    result = {"error": "未知的动作类型"}
                
                result["frame"] = frame_count
                analysis_results.append(result)
            
            frame_count += 1
        
        cap.release()
        
        # 生成BVH数据
        bvh_data = self.bvh_converter.keypoints_to_bvh(keypoints_sequence)
        
        # 综合评分
        valid_scores = [r["score"] for r in analysis_results if "score" in r]
        avg_score = np.mean(valid_scores) if valid_scores else 0
        
        result = {
            "video_path": video_path,
            "action_type": action_type,
            "total_frames": frame_count,
            "analyzed_frames": len(analysis_results),
            "average_score": avg_score,
            "frame_results": analysis_results,
            "bvh_data": bvh_data,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"✅ 视频处理完成, 平均分数: {avg_score:.2f}")
        return result


if __name__ == "__main__":
    # 测试示例
    motion_capture = FitnessMotionCapture()
    
    # 模拟分析结果
    test_result = {
        "action_type": "squat",
        "average_score": 85.5,
        "feedback": ["动作基本标准", "建议膝关节弯曲角度再深一些"],
        "timestamp": datetime.now().isoformat()
    }
    
    # 保存结果
    with open('data/processed/motion_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(test_result, f, ensure_ascii=False, indent=2)
    
    logger.info("✅ 动作分析完成!")
