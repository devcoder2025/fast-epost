from sklearn.model_selection import train_test_split
import tensorflow as tf

class WatchlistTrainer:
    def __init__(self):
        self.model = self.build_model()
        self.batch_size = 32
        self.epochs = 10
        
    def build_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Embedding(10000, 64),
            tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
        model.compile(optimizer='adam',
                     loss='binary_crossentropy',
                     metrics=['accuracy'])
        return model
        
    def train(self, X, y):
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)
        
        print("Starting model training...")
        history = self.model.fit(
            X_train, y_train,
            batch_size=self.batch_size,
            epochs=self.epochs,
            validation_data=(X_val, y_val)
        )
        print("Training completed!")
        return history
