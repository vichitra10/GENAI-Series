WebBaseLoader and CSVLoader

WebBaseLoader: This loads and extracts the content and text from the web-page and web-url. It uses beautifulsoup library to parse html and extract visible data. 
When to use:  We should use for Blogs , News Article and Public websites. These should be primarly text-based and static 
WebBase Loader only loads static -content as whats in the HTML , not what loads after the page Render.


CSVLoader: It used to load CSV Files into langchain document object 
No of documents: Total rows in CSV files 



Length Based Text Splitting: It is the fastest text splitting . Here we split the data where we already decide that how many character or how many tokens we need to have in every chunk. 

