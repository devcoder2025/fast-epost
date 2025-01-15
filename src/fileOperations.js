import fs from 'fs/promises';

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

export const batchProcessFiles = async (filePaths) => {
  const results = [];
  for (const filePath of filePaths) {
    try {
      const data = await readFileAsync(filePath);
      results.push(data);
    } catch (error) {
      console.error(`Error processing file ${filePath}:`, error);
    }
  }
  return results;
};
