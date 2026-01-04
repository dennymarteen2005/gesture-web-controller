from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

# Ground truth labels (what YOU intended to show)
# Example: You show gestures in this order manually
y_true = [
    "PLAY_PAUSE", "PLAY_PAUSE", "SCROLL_DOWN", "NEXT",
    "PLAY_PAUSE", "PREV", "SCROLL_DOWN", "NEXT",
    "PLAY_PAUSE", "PREV"
]

# Predicted labels (what system detected)
# These come from your controller logs
y_pred = [
    "PLAY_PAUSE", "PLAY_PAUSE", "SCROLL_DOWN", "NEXT",
    "PLAY_PAUSE", "SCROLL_DOWN", "SCROLL_DOWN", "NEXT",
    "PLAY_PAUSE", "PREV"
]

print("Accuracy :", accuracy_score(y_true, y_pred))
print("Precision:", precision_score(y_true, y_pred, average="macro"))
print("Recall   :", recall_score(y_true, y_pred, average="macro"))
print("F1 Score :", f1_score(y_true, y_pred, average="macro"))

print("\nDetailed Report:\n")
print(classification_report(y_true, y_pred))
