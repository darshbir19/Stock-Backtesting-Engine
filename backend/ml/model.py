import numpy as np
from backend.data import fetch
from backend.strategies import moving_average , rsi
from sklearn import preprocessing
import pickle

def prepare_features(df):
    df = moving_average.moving_average_crossover(df)
    df = rsi.rsi(df)
   
    df.dropna(inplace=True)
    return df[['Close', 'Volume', 'RSI', 'stma', 'ltma']]
    
def create_sequences(feature_df, sequence_length=60):
    scaler =  preprocessing.MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(feature_df)
    X = []
    y = []

    for i in range(len(scaled_data) - sequence_length):
        X.append(scaled_data[i : i + sequence_length]) 
        y.append(np.where(scaled_data[i + sequence_length][0] > scaled_data[i + sequence_length - 1][0], 1, 0))  

    return np.array(X), np.array(y), scaler



def build_model(sequence_length=60, n_features=5):
    from tensorflow.keras.layers import LSTM, Dropout, Dense
    from tensorflow.keras.models import Sequential

    model = Sequential()

    model.add(
        LSTM(
            128,
            return_sequences=True,
            input_shape=(sequence_length, n_features)
        )
    )

    model.add(Dropout(0.2))

    model.add(
        LSTM(
            64,
            return_sequences=False
        )
    )

    model.add(Dropout(0.2))

    model.add(Dense(32, activation="relu"))

    model.add(Dense(1, activation="sigmoid"))

    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )

    return model
    


if __name__ == "__main__":
    df = fetch.fetch_stock_data("AAPL")
    feature_df = prepare_features(df)
    X, y, scaler = create_sequences(feature_df)
    
    # train/test split 80/20
    split = int(len(X) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    
    model = build_model()
    model.summary()
    
    model.fit(
        X_train, y_train,
        epochs=10,
        batch_size=32,
        validation_data=(X_test, y_test)
    )
    model.save('backend/ml/saved_model.keras')
   
    with open('backend/ml/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
