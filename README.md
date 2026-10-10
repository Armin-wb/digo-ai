🤖 Digo AI

An AI-Powered Telegram Group Assistant

Digo AI is a Python-based Telegram bot that brings AI-powered assistance directly into Telegram groups. It uses configurable AI APIs to generate Persian responses and provides administrative tools for managing users, paid subscriptions, usage limits, and broadcast messages.

Its main feature is a simple, reply-based workflow: a group administrator replies to a user's question, mentions Digo, and the bot sends an AI-generated answer as a reply to the original message.

Digo AI combines intelligent question answering with practical administrative controls, making it a useful solution for Telegram communities that want AI assistance without unnecessary interruptions to group conversations.

---

✨ Features

Feature| Description
🧠 AI Integration| Generate responses using configurable AI APIs.
💬 Telegram Groups| Answer questions directly inside group conversations.
↩️ Reply-Based Interaction| Respond to a user's message when an administrator replies and mentions Digo.
🇮🇷 Persian Responses| Designed to provide answers in Persian.
👥 User Management| Manage bot users through administrative commands.
💎 Subscription Management| Support paid subscriptions with configurable durations in days.
📊 Usage Limits| Manage usage limits for users.
📢 Broadcast Messaging| Send messages to multiple bot users.
⚙️ Command-Based Administration| Manage supported bot features through Telegram commands.

---

🚀 How It Works

Digo AI uses an administrator-triggered workflow to answer questions in Telegram groups.

1. A user asks a question in a Telegram group.
2. A group administrator replies directly to that message.
3. The administrator mentions the bot by calling its name: Digo.
4. Digo processes the question using the configured AI API.
5. The bot generates a response in Persian.
6. The generated answer is sent as a reply to the original message.

This workflow keeps conversations organized and gives group administrators control over when the bot responds.

💡 Example Interaction

User:

«پایتون چیست و چه کاربردی دارد؟»

Group administrator:

Replies to the user's message and mentions "Digo".

Digo AI:

«پایتون یک زبان برنامه‌نویسی سطح بالا و چندمنظوره است که به دلیل سادگی یادگیری، خوانایی بالا و اکوسیستم گسترده، در توسعه وب، اتوماسیون، تحلیل داده و هوش مصنوعی کاربرد دارد.»

This example illustrates the intended interaction. Actual responses depend on the configured AI provider and model.

---

🛠️ Technology Stack

Technology| Purpose
Python| Core application logic
Telegram Bot API| Telegram communication and message handling
Configurable AI APIs| AI-powered response generation
Telegram Bot Commands| Administrative controls and management

---

📦 Installation

Prerequisites

Before installing Digo AI, make sure you have:

- Python installed on your system.
- A Telegram bot token obtained through "@BotFather" (https://t.me/BotFather).
- An API key for a supported AI provider.
- Git installed on your system.
- Access to the project's source code and required dependencies.

1. Clone the Repository

Clone the public repository:

git clone https://github.com/Armin-wb/digo-ai.git
cd digo-ai

2. Create a Virtual Environment

Create an isolated Python environment:

python -m venv .venv

Windows:

.venv\Scripts\activate

Linux / macOS:

source .venv/bin/activate

3. Install Dependencies

If the project includes a "requirements.txt" file, install the required packages:

pip install -r requirements.txt

If no dependency file is provided, inspect the source code to identify the required packages before installing them.

4. Configure Environment Variables

Digo AI requires a Telegram bot token and credentials for its configured AI provider.

A possible configuration template is shown below:

TELEGRAM_BOT_TOKEN=your_telegram_bot_token
AI_API_KEY=your_ai_api_key
AI_API_BASE_URL=your_ai_api_base_url
AI_MODEL=your_ai_model

Important: These variable names are examples, not verified configuration keys. Use the exact variable names and settings expected by the implementation. Some providers may not require a custom API base URL or model variable.

Keep your credentials private and never publish real API keys or bot tokens in a public repository.

5. Run the Bot

The repository currently contains the Python source file "V8.py".

If this file is the application entry point and the required dependencies and configuration are ready, start the bot using:

python V8.py

The actual startup command depends on the application's implementation.

---

⚙️ Configuration

Digo AI is designed around configurable AI integration and Telegram-based administration.

Depending on the implementation, configuration may include:

- Telegram bot credentials.
- AI provider credentials.
- AI model and API settings.
- Subscription durations and access rules.
- Per-user usage limits.
- Administrator permissions.
- Broadcast messaging options.

Refer to the source code and implemented administrative commands for the exact configuration options available in your version.

---

👑 Administration

Digo AI includes administrative functionality to help manage users and control access to the bot.

Management Area| Purpose
User Management| Manage bot users through supported administrative controls.
Subscription Management| Configure paid access and subscription durations.
Usage Limits| Control user access according to implemented usage rules.
Broadcast Messaging| Distribute messages to multiple bot users.
Group Responses| Trigger AI-generated answers through replies and mentions.

The exact command names, arguments, and permission requirements depend on the implementation.

For secure operation, administrative commands should be restricted to authorized users.

---

💎 Subscription Management

Digo AI supports paid subscription management with durations configured in days.

Subscription management can help administrators organize access to the bot according to defined subscription periods.

Depending on the implemented functionality, subscription policies may define:

- Subscription duration.
- User access periods.
- Usage restrictions.
- Subscription expiration rules.

Pricing, payment processing, automatic renewals, and payment verification should not be assumed unless they are explicitly implemented in the project.

---

📊 Usage Management

Usage limits provide a way to control how users interact with the bot.

Managing usage can help administrators establish reasonable limits and control consumption of AI API resources.

The available limits, enforcement rules, and their relationship to subscriptions depend on the implementation.

---

📢 Broadcast Messaging

Digo AI includes broadcast messaging functionality for communicating with multiple bot users.

Broadcast messages may be useful for:

- Announcing service updates.
- Sharing important information.
- Communicating administrative notices.
- Informing users about relevant changes.

Broadcast operations should be used responsibly and restricted to authorized administrators. Delivery depends on Telegram permissions, recipient availability, and applicable platform restrictions.

---

🔐 Security Best Practices

Security is important for any Telegram bot that uses external AI services and provides administrative functionality.

🔑 Protect Credentials

Never publish real Telegram bot tokens, AI API keys, passwords, or other sensitive credentials.

Use environment variables or an appropriate secret-management system to protect credentials.

🛡️ Restrict Administrative Access

Ensure that sensitive operations, including user management and broadcast messaging, are accessible only to authorized administrators.

Validate permissions on the server side rather than relying on command visibility alone.

🔒 Protect User Information

Store and process only the information necessary for the bot's operation.

Avoid exposing private user data through logs, public error messages, or broadcast operations.

💰 Monitor API Usage

AI APIs may incur costs depending on the provider and usage.

Use the available usage controls and review API consumption to reduce unexpected expenses.

📁 Secure the Repository

Before publishing code, verify that sensitive files are excluded from version control.

Common files and data to protect include:

- ".env" files.
- Local configuration files containing secrets.
- Private database files.
- Logs containing sensitive information.
- API credentials and bot tokens.

A ".gitignore" file can help prevent accidental commits, but it does not remove secrets already present in Git history.

If a token or API key is exposed, revoke it and generate a replacement immediately.

---

🗺️ Project Roadmap

Potential future improvements include:

- Expanded AI provider configuration.
- More detailed subscription and usage reporting.
- Improved administrative controls.
- More flexible group-specific settings.
- Enhanced documentation and deployment guidance.
- Additional testing and maintenance tools.

These are possible future development directions, not claims about features currently available.

---

🤝 Contributing

Contributions, suggestions, and bug reports are welcome.

If you would like to contribute to Digo AI:

1. Fork the repository.
2. Create a branch for your changes.
3. Implement and test your changes.
4. Submit a pull request describing your improvements.

Please keep contributions focused, document relevant changes, and avoid including credentials or private user data.

---

🐛 Bug Reports and Suggestions

If you encounter a problem or have an idea for improvement, consider opening an issue in the GitHub repository.

When reporting a bug, provide:

- A clear description of the issue.
- Steps to reproduce the problem.
- Relevant error messages with sensitive information removed.
- Your Python version and relevant environment details.

Never include API keys, bot tokens, passwords, or private user information in public issues.

---

📄 License

Check the repository for an existing "LICENSE" file to determine the project's licensing terms.

If no license has been provided, do not assume that the code is licensed for unrestricted reuse, modification, or redistribution.

---

👨‍💻 About the Project

Digo AI is a Python-based Telegram bot project focused on combining AI-powered question answering with practical group administration tools.

By connecting configurable AI APIs with a reply-based Telegram workflow, Digo aims to make AI assistance easier to access while keeping group administrators in control of when responses are generated.

Repository: "Armin-wb/digo-ai" (https://github.com/Armin-wb/digo-ai)

---

<p align="center">
  <strong>🤖 Digo AI</strong>
  <br>
  <em>Intelligent Answers. Simple Interactions. Better Communities.</em>
</p>
