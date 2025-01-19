import { StatusBar } from 'expo-status-bar';
import { useEffect } from 'react'; // Importing useEffect
import { StyleSheet, Text, View } from 'react-native';
import Dashboard from './components/Dashboard'; // Importing Dashboard component
import LoadingScreen from './components/LoadingScreen'; // Importing LoadingScreen component
import React, { useState } from 'react'; // Importing useState

export default function App() { 
  const [loading, setLoading] = useState(true); // State to manage loading

  useEffect(() => {
    // Simulate loading process
    const timer = setTimeout(() => {
      setLoading(false); // Update loading state after 2 seconds
    }, 2000);
    
    return () => clearTimeout(timer); // Cleanup timer on unmount
  }, []);

  const handleLoadingComplete = () => {
    setLoading(false); // Update loading state
  };

  return ( 
    <View style={styles.container}>
      {loading ? (
        <LoadingScreen onLoadingComplete={handleLoadingComplete} /> // Show loading screen
      ) : (
        <Dashboard /> // Show Dashboard component
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
