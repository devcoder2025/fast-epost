import { readFileAsync, writeFileAsync, deleteFileAsync, batchProcessFiles } from './fileOperations';
import fs from 'fs/promises';

jest.mock('fs/promises');

describe('File Operations', () => {
  const testFilePath = 'test.txt';
  const testContent = 'Hello, World!';

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('reads a file asynchronously', async () => {
    fs.readFile.mockResolvedValue(testContent);
    const data = await readFileAsync(testFilePath);
    expect(data).toBe(testContent);
    expect(fs.readFile).toHaveBeenCalledWith(testFilePath, 'utf-8');
  });

  test('writes to a file asynchronously', async () => {
    await writeFileAsync(testFilePath, testContent);
    expect(fs.writeFile).toHaveBeenCalledWith(testFilePath, testContent, 'utf-8');
  });

  test('deletes a file asynchronously', async () => {
    await deleteFileAsync(testFilePath);
    expect(fs.unlink).toHaveBeenCalledWith(testFilePath);
  });

  test('processes multiple files in batch', async () => {
    const filePaths = ['file1.txt', 'file2.txt'];
    const fileContents = ['Content 1', 'Content 2'];
    fs.readFile.mockResolvedValueOnce(fileContents[0]).mockResolvedValueOnce(fileContents[1]);

    const results = await batchProcessFiles(filePaths);
    expect(results).toEqual(fileContents);
    expect(fs.readFile).toHaveBeenCalledTimes(filePaths.length);
  });

  test('handles errors during batch processing', async () => {
    const filePaths = ['file1.txt', 'file2.txt'];
    fs.readFile.mockRejectedValueOnce(new Error('Error reading file'));

    const results = await batchProcessFiles(filePaths);
    expect(results).toEqual([undefined, 'Content 2']); // Assuming the second file reads successfully
  });
});
