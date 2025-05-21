# Naukri Profile Auto-Updater

This tool automatically updates your Naukri profile bio daily by alternating between adding and removing spaces. This keeps your profile active and potentially improves visibility in job searches.

## Features

- Automatically logs in to your Naukri account
- Updates your profile bio by either adding spaces between characters or removing them
- Alternates between these two states daily
- Maintains a state file to track which type of update was performed last
- Provides detailed logging for monitoring

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   npm install
   ```
3. Create a `.env` file based on the `.env.example` template:
   ```
   cp .env.example .env
   ```
4. Edit the `.env` file to add your Naukri credentials:
   ```
   NAUKRI_EMAIL=your_email@example.com
   NAUKRI_PASSWORD=your_password
   ```

## Usage

### Running manually

To run the updater once immediately:

```
npm start -- --now
```

### Running on a schedule

To start the scheduled updates (default is daily at 9 AM):

```
npm start
```

You can customize the schedule by changing the `CRON_SCHEDULE` value in your `.env` file. The format is a standard cron expression.

## Running as a service

To keep this running continuously on a server, you may want to use a process manager like PM2:

```
npm install -g pm2
pm2 start src/index.js --name "naukri-updater"
pm2 save
pm2 startup
```

## Troubleshooting

Check the logs in the `logs` directory for any errors or issues. The `error.log` file contains only errors, while `combined.log` contains all log messages.

## Security Note

This tool requires your Naukri login credentials. These are stored in the `.env` file, which is excluded from version control. Never share this file or commit it to a repository.