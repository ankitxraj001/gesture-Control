def count_fingers(hand_landmarks):
    finger_tips = [8, 12, 16, 20]
    count = 0
    for tip in finger_tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            count += 1
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        count += 1
    return count

def get_gesture(hand_landmarks):
    fingers = count_fingers(hand_landmarks)
    wrist_y = hand_landmarks.landmark[0].y
    index_tip_y = hand_landmarks.landmark[8].y
    thumb_tip = hand_landmarks.landmark[4]
    index_tip = hand_landmarks.landmark[8]
    pinch_distance = abs(thumb_tip.x - index_tip.x) + abs(thumb_tip.y - index_tip.y)
    if fingers == 0:
        return "STOP"
    elif fingers == 1:
        if index_tip_y < wrist_y - 0.15:
            return "SCROLL_UP"
        elif index_tip_y > wrist_y + 0.05:
            return "SCROLL_DOWN"
    elif fingers == 2:
        return "SCROLL_UP_FAST"
    elif fingers == 5:
        return "STOP"
    if pinch_distance < 0.05:
        return "CLICK"
    return "NONE"
