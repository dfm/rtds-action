const core = require("@actions/core");
const github = require("@actions/github");
const fetch = require("node-fetch");

try {
  // `who-to-greet` input defined in action metadata file
  const webhookId = core.getInput("webhook_id");
  const webhookToken = core.getInput("webhook_token");
  const ref = github.context.payload.ref;

  const url = `https://readthedocs.org/api/v2/webhook/${webhookId}/`;
  const params = new URLSearchParams();
  params.append("branches", "main");
  params.append("token", webhookToken);

  console.log(`The event ref: ${ref}`);
} catch (error) {
  core.setFailed(error.message);
}
