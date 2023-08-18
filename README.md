# YTSC

YTSC is a Python app for seeing the most recent uploaded videos on a particular search term paginated by timestamp

Done for the Fampay backend task

## Salient Features

1. Uses the YouTube API v3 to get data about videos and store them in a database in a background async process
2. The database used is MongoDB
3. MongoDB collection is used in timeseries mode so you can leverage clever features like
   - data expiry by timestamp field
   - very fast search queries due to the index on the timestamp field
4. Automatic Spin down of the background process to save YouTube API quota
5. Ability to evenly distribute YouTube API requests among multiple API keys
6. REST API which provides paginated results to videos on the basis of timestamp
7. Dashboard is dynamically paginated by published time of the videos uploaded with infinite scrolling implemented

## Installation

Step 1: Clone the repo

```bash
git clone https://github.com/fa993/fampay-task.git
```

Step 2: Move into the repo

```bash
cd fampay-task
```

Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

Step 4: Setup the .env file and save it in this directory

Step 5: Run the app

```bash
flask run
```

## Usage

Navigate to http://127.0.0.1:5000/ to see the dashboard

## License

[MIT](https://choosealicense.com/licenses/mit/)
