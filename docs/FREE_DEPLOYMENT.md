# Free cloud demo (Hugging Face Docker Spaces)

This is a restricted-access portfolio demonstration, not a production service. Free CPU Basic hardware is subject to availability, sleep and temporary filesystem storage. Never upload confidential material. The Docker image trains the baseline from the public dataset during build; the build requires dataset availability.

1. Create a free Hugging Face account and a new Space. Select Docker SDK, CPU Basic (free) hardware and a public Space. Do not select paid hardware or storage.
2. In Space Settings → Variables and secrets, add PROMPTGUARD_API_KEY (32+ random characters). Keep these private.
3. Copy the source tree from GitHub into the Space with Git. Use the repository's Dockerfile.cloud as the Space root Dockerfile. Set README front matter to sdk: docker and app_port: 7860. See the exact PowerShell steps in the chat deployment guide or use the Space Git URL and a write-scoped token via credential prompts. Never commit .env, credentials, databases, uploaded documents or local model files.
4. After the build completes, open the Space application. Enter the private admin API key and analyze a synthetic benign prompt.
5. Check /api/v1/health and the application's relevant features. Storage and accounts may reset on restart. Do not advertise a live URL until it has been tested.

The separate Dockerfile.cloud packages React and FastAPI in one service. The default local Docker Compose workflow is unchanged. No hosted LLM API is required. Public use needs further security hardening and resource controls.
