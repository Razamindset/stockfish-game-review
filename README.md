# Chess Game Review Engine

Welcome to the **Chess Game Review Engine** project! This project allows developers to analyze FENs (Forsyth-Edwards Notation) using the Stockfish chess engine. It supports two modes of operation: single-threaded and multi-threaded analysis. Choose the one that suits your needs or experiment with both!

## Features

- **Single-threaded analysis:** Run the Stockfish engine in a single thread for simpler resource usage. This is ideal for smaller datasets or environments where minimal resource consumption is required.
- **Multi-threaded analysis:** Run Stockfish using multiple threads to achieve **2x speed improvement** at the cost of **4x higher resource usage**. Ideal for handling large datasets or situations requiring faster performance.

## How to Set Up

1. **Install Dependencies:**

   - Clone the repository and navigate to the project folder.
   - Create a virtual environment and install dependencies:

     ```bash
     python -m venv venv
     .\venv\Scripts\activate  # For Windows
     pip install -r requirements.txt
     ```

2. **Download Stockfish:**
   - Visit the [official Stockfish website](https://stockfishchess.org/download/) and download the appropriate version for your operating system.
   - Rename the downloaded file to `stockfish.exe`.
   - Place the `stockfish.exe` file in the root folder of this project.

2. **Running the Engine:**
   You can run the engine in either of two modes:

   - **Single-threaded analysis**:

     ```bash
     python src/single_py_thread.py
     ```

   - **Multi-threaded analysis**:

     ```bash
     python src/multi_py_thread.py
     ```

   Both implementations will analyze the FENs and output the best moves computed by Stockfish.

## Performance Considerations

- **Single-threaded mode** is suitable for environments where resources are limited or where analysis of smaller datasets is sufficient.
- **Multi-threaded mode** will result in faster processing (up to **2x faster**) but requires more system resources (**4x more**).

Feel free to experiment with both versions and choose the one that best fits your project’s needs.

## Contributions

Feel free to contribute to this project! You can:

- Improve the performance.
- Add more features (e.g., UI integration, additional analysis metrics, etc.).
- Submit bug reports and fixes.

We are currently working on optimizing performance and will provide additional documentation and examples soon. Move feedback will soon be added wit full game report.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
