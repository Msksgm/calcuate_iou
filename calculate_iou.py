import pdb
import argparse


def calculate_pos2neg(pred_boxes, gt_boxes, iou_thresh):
    pos_num = 0
    while pred_boxes != [[]] and gt_boxes != [[]]:
        thresh = -float("inf")
        for pred in pred_boxes:
            for gt in gt_boxes:
                x1 = max(pred[0], gt[0])
                y1 = max(pred[1], gt[1])
                x2 = min(pred[2], gt[2])
                y2 = min(pred[3], gt[3])

                if x2 < x1 or y2 < y1:
                    continue

                # calculate Intersection over Union
                sq_c = (x2 - x1) * (y2 - y1)
                sq_a = (pred[2]-pred[0])*(pred[3]-pred[1])
                sq_b = (gt[2]-gt[0])*(gt[3]-gt[1])
                sum_ab = sq_a + sq_b - sq_c
                iou = float(sq_c) / float(sum_ab)

                if iou == max(thresh, iou):
                    thresh = iou
                    pred_rm = pred
                    gt_rm = gt

                if iou > 1.0 or iou < 0.0:
                    pdb.set_trace()

        # if iou's thresh hold is lower than iou_thresh hold, break for loop
        if thresh < iou_thresh:
            break

        # if predict bounding boxes or gt_boxes is [], break for loop
        if pred_boxes == [] or gt_boxes == []:
            break

        pred_boxes.remove(pred_rm)
        gt_boxes.remove(gt_rm)
        pos_num += 1
    return pos_num


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--iou_thresh", type=float, default=0.5)
    args = parser.parse_args()
    return args


def main():
    # setting args
    args = parse_args()
    iou_thresh = args.iou_thresh

    # setting pred coordinates
    pred_coords = [[[132, 126, 600, 535], [156, 269, 416, 394], [205, 322, 306, 394], [446, 197, 639, 512], [227, 300, 459, 535], [453, 123, 619, 196], [465, 123, 523, 180], [443, 130, 502, 213], [569, 0, 594, 10], [549, 0, 576, 10], [507, 0, 639, 33], [588, 0, 610, 10], [524, 0, 564, 15]], [[0, 365, 426, 639], [282, 189, 299, 241], [275, 219, 288, 241], [214, 182, 292, 237], [228, 261, 267, 278]], [[]], [[274, 183, 378, 279], [328, 177, 359, 281], [362, 228, 639, 406], [317, 195, 378, 234], [426, 228, 475, 274], [283, 165, 323, 213], [306, 204, 338, 279], [367, 225, 456, 270], [325, 200, 351, 224]]]

    # setting ground truth coordinates
    gt_coords = [[[249, 108, 632, 536], [69, 126, 368, 412], [6, 24, 360, 529], [161, 173, 251, 391]], [[165, 108, 395, 380], [207, 238, 255, 288]], [[7, 3, 427, 628], [220, 237, 323, 310]], [[263, 248, 302, 338], [83, 256, 121, 322]], [[7, 3, 427, 628], [220, 237, 323, 310]], [[404, 204, 524, 418], [273, 112, 306, 134], [272, 153, 373, 424], [185, 234, 278, 420]]]

    for i, (pred_boxes, gt_boxes) in enumerate(zip(pred_coords, gt_coords)):
        pos_num = 0
        pred_num = len(pred_boxes)
        gt_num = len(gt_boxes)
        pos_num += calculate_pos2neg(pred_boxes, gt_boxes, iou_thresh)
        print("number", "TP", "FP", "TN")
        print([i, str(pos_num), str(pred_num-pos_num), str(gt_num-pos_num)])


if __name__ == "__main__":
    main()
