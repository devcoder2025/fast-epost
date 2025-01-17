import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';
import LoadingScreen from './components/LoadingScreen'; // Importing LoadingScreen component
import React, { useState } from 'react'; // Importing useState

export default function App() { 
  const [loading, setLoading] = useState(true); // State to manage loading

  const handleLoadingComplete = () => {
    setLoading(false); // Update loading state
  };

  return ( 
    <View style={styles.container}>
      {loading ? (
        <LoadingScreen onLoadingComplete={handleLoadingComplete} /> // Show loading screen
      ) : (
        <Text>Open up App.js to start working on your app!</Text>
      )}
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({ 
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
