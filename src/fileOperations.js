import fs from 'fs/promises'; // Importing file system promises
import path from 'path'; // Importing path module for file path operations

// Function to read a file asynchronously
export const readFileAsync = async (filePath) => {
  try {
    const data = await fs.readFile(filePath, 'utf-8');
    return data;
  } catch (error) {
    console.error('Error reading file:', error);
    throw error;
  }
};

// Function to write to a file asynchronously
export const writeFileAsync = async (filePath, content) => {
  try {
    await fs.writeFile(filePath, content, 'utf-8');
  } catch (error) {
    console.error('Error writing to file:', error);
    throw error;
  }
};

// Function to delete a file asynchronously
export const deleteFileAsync = async (filePath) => {
  try {
    await fs.unlink(filePath);
  } catch (error) {
    console.error('Error deleting file:', error);
    throw error;
  }
};

// Function to process multiple files concurrently
export const batchProcessFiles = async (filePaths) => {
  const results = await Promise.all(filePaths.map(async (filePath) => {
    try {
      return await readFileAsync(filePath);
    } catch (error) {
      console.error(`Error processing file ${filePath}:`, error);
      return null; // Return null for failed operations
    }
  }));
  return results.filter(result => result !== null); // Filter out null results
};
