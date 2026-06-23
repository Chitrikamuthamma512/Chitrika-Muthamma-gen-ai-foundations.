# Question 1: The Vector Conflict

Yes, the similarity score showed that two sentences using the word "light" could still appear similar even when they meant completely different things. This happens because CountVectorizer only counts how many times words appear and does not understand their meaning. Since both sentences contain the word "light", the model assumes there is a relationship between them. As a result, it creates a misleading similarity score even though the contexts are different.


# Question 2: The Context Blindspot

From a Data Science perspective, the Bag-of-Words approach is limited because it ignores the context in which words are used. Search engines and chatbots need to understand the meaning of words to provide accurate results, but static word counts cannot do this. Important information such as word order, context, and semantic meaning is lost during vectorization. This makes it difficult for the system to correctly interpret user queries and conversations.


# Question 3: The GenAI Architectural Fix

Modern Large Language Models like GPT and LLaMA overcome this problem by using Context-Aware Embeddings and Masked Self-Attention. Self-attention helps the model focus on surrounding words to understand the intended meaning of a word within a sentence. Because of this, the word "light" in a sentence about food gets a different vector representation than "light" in a sentence about brightness. This context-based understanding allows LLMs to process language much more accurately than traditional Bag-of-Words methods.
