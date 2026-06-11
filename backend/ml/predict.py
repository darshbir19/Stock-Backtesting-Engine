import numpy as np
import pickle

from backend.ml.model import prepare_features


def load_lstm_model(path):
    try:
        from tensorflow.keras.models import load_model
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "LSTM strategy requires TensorFlow. Install it in the backend "
            "environment with: pip install tensorflow"
        ) from exc

    return load_model(path)


def generate_lstm_signals(df, sequence_length=60):

    # Load trained model
    model = load_lstm_model("backend/ml/saved_model.keras")

    # Load scaler
    with open("backend/ml/scaler.pkl", "rb") as f:
        scaler = pickle.load(f)

    # Prepare features
    feature_df = prepare_features(df.copy())

    # Scale using training scaler
    scaled_data = scaler.transform(feature_df)

    # Create rolling sequences
    X = []

    for i in range(len(scaled_data) - sequence_length):
        X.append(scaled_data[i:i + sequence_length])

    X = np.array(X)

    # Predict probabilities
    probabilities = model.predict(X, verbose=0).flatten()

    # Convert probabilities to signals
    signals = [np.nan] * sequence_length

    for prob in probabilities:
        if prob > 0.6:
            signals.append(1)
        elif prob < 0.4:
            signals.append(-1)
        else:
            signals.append(0)

    # Add Signal column
    feature_df["Signal"] = signals

    return feature_df


if __name__ == "__main__":
    from backend.data import fetch
    df = fetch.fetch_stock_data("AAPL")
    result = generate_lstm_signals(df)
    print(result[['Close', 'Signal']].tail(20))
