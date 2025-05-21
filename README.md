# Naukri Profile Auto-Updater

This tool automatically updates your Naukri profile bio daily by alternating between adding and removing spaces. This keeps your profile active and potentially improves visibility in job searches.

## Features

- Automatically logs in to your Naukri account
- Updates your profile bio by either adding spaces between characters or removing them
- Alternates between these two states daily
- Maintains a state file to track which type of update was performed last
- Provides detailed logging for monitoring
- Supports both local execution and AWS Lambda deployment

## Local Setup

1. Clone this repository
2. Install dependencies:
   ```
   npm install
   ```
3. Create a `.env` file based on the `.env.example` template:
   ```
   cp .env.example .env
Naukri credentials:
   ```
   NAUKRI_EMAIL=your_email@example.com
   NAUKRI_PASSWORD=your_password
   ```

## Local Usage

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

## AWS Lambda Deployment

### Prerequisites

1. Install AWS CLI and configure with your credentials:
   ```bash
   aws configure
   ```

2. Store Naukri credentials in AWS Systems Manager Parameter Store:
   ```bash
   aws ssm put-parameter --name "/naukri/email" --value "your-email" --type SecureString
   aws ssm put-parameter --name "/naukri/password" --value "your-password" --type SecureString
   ```

### Deployment Steps

1. Create a Lambda function:
   - Runtime: Node.js 18.x
   - Memory: 1024 MB (minimum)
   - Timeout: 5 minutes
   - Architecture: x86_64

2. Build the deployment package:
   ```bash
   npm run build
   ```

3. Deploy to Lambda:
   ```bash
   aws lambda update-function-code --function-name naukri-updater --zip-file fileb://function.zip
   ```

4. Set up daily trigger using EventBridge (CloudWatch Events):
   ```bash
   aws events put-rule --name "NaukriDailyUpdate" --schedule-expression "cron(0 9 * * ? *)"
   aws events put-targets --rule NaukriDailyUpdate --targets "Id"="1","Arn"="YOUR_LAMBDA_ARN"
   ```

### Lambda Configuration Requirements

1. IAM Role Permissions:
   - `ssm:GetParameter` for accessing credentials
   - `logs:CreateLogGroup`
   - `logs:CreateLogStream`
   - `logs:PutLogEvents`

2. Environment Variables:
   - None required (credentials are fetched from Parameter Store)

## Troubleshooting

Check the logs in CloudWatch Logs (for Lambda) or the `logs` directory (for local execution) for any errors or issues. The `error.log` file contains only errors, while `combined.log` contains all log messages.

## Security Note

This tool requires your Naukri login credentials. For local deployment, these are stored in the `.env` file, which is excluded from version control. For AWS Lambda deployment, credentials are securely stored in AWS Systems Manager Parameter Store. Never share or commit sensitive credentials.