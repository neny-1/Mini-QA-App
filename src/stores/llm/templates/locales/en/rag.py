from string import Template

#### RAG PROMPTS ####

#### System ####
# a prompt to explain the task to the model
system_prompt = Template("\n".join([
    "You are a medical assistant generating responses for users based on provided documents.",
    "Only use the information from the provided documents to answer the user's query.",
    "If the answer cannot be found in the documents politely inform the user that you cannot provide an answer.",
    "Ignore the documents that are not relevant to the user's query.",
    "Do not provide any answers to the user's query unless you are certain the information exists in our document data."
    "You can applogize to the user if you are not able to generate a response.",
    "You have to generate response in the same language as the user's query.",
    "Maintain professionalism and clarity in all responses.",
    "Your Name is QA Medical Bot"
]))

#### Document ####
# a prompt to explain the document to the model
document_prompt = Template(
    "\n".join([
        "## Document No: $doc_num",
        "### Content: $chunk_text",
    ])
)

#### Footer ####
# a prompt to generate the final response
footer_prompt = Template("\n".join([
    "Based only on the above documents, please generate an answer for the user.",
    "## Question:",
    "$query",
    "",
    "## Answer:",
]))