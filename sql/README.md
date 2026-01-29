# SQL Configuration Files

## Overview

This directory contains SQL scripts for database setup and configuration.

## Configuration Template

### `tb_config.template.sql`

This is a template file containing obfuscated configuration values for the `tb_global_configuration` table. It can be safely committed to version control as it does not contain any sensitive information.

### How to Use

1. **Copy the template file:**
   ```bash
   cp sql/tb_config.template.sql sql/tb_config.sql
   ```

2. **Replace placeholder values** in `tb_config.sql` with your actual configuration:
   - `YOUR_OPENAI_API_KEY_HERE` → Your OpenAI API key
   - `YOUR_GRAPHRAG_JWT_TOKEN_HERE` → Your GraphRAG JWT token
   - `YOUR_JWT_SECRET_HERE` → Your JWT secret key
   - `YOUR_SMTP_PASSWORD_HERE` → Your SMTP password
   - `YOUR_SMTP_USERNAME_HERE` → Your SMTP username
   - `YOUR_LANGCHAIN_API_KEY_HERE` → Your LangChain API key
   - Update email addresses, URLs, and paths as needed

3. **Import into your database:**
   ```bash
   psql -U your_user -d your_database -f sql/tb_config.sql
   ```

### Security Note

⚠️ **Important:** The actual `tb_config.sql` file is gitignored and should **never** be committed to version control as it contains sensitive secrets and API keys.

### Configuration Keys

The template includes the following configuration categories:

- **API Keys & Secrets:** OpenAI, LangChain, JWT, GraphRAG
- **Email Configuration:** SMTP server, credentials, sender information
- **Application Settings:** Message limits, timeouts, model configurations
- **File Paths:** Project root, cache folders, PDF folders
- **Feature Flags:** GraphRAG usage, streaming, caching options

### Updating the Template

If you add new configuration keys to the database, please update `tb_config.template.sql` with obfuscated placeholder values so other developers know what needs to be configured.
