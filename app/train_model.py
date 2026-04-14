print("TOP OF train_model.py")

from .model import train_and_save_model

print("IMPORT SUCCESS")


def main():
    print("INSIDE MAIN")

    try:
        model, metrics = train_and_save_model()

        print("\nMODEL TRAINED AND SAVED")
        print("\nAccuracy:", metrics.get("accuracy", "N/A"))
        print("\nConfusion Matrix:")
        print(metrics.get("confusion_matrix", "N/A"))
        print("\nClassification Report:")
        print(metrics.get("classification_report", "N/A"))

    except Exception as e:
        print("\nERROR IN TRAINING:", str(e))


if __name__ == "__main__":
    main()