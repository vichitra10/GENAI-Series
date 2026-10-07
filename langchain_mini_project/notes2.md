Documents Loaders

We have multiple type of documents loaders which are
Text Loader
PyPdf Loader
Web-Based Loader
CSV Loader


Text Loaders:  It is being used to gather the data from a .txt file format.
How its works like : plain-text ----> Text Loader ----> Convert -----> Document Object

Use Cases: Ideal for loading chat-logs, Scraped-text, Transscripts Code snippets or any other Plain text file.  



PYPdf Loader: It helps for working with text only content in PDF File

Use Cases

1)  Simple, clean text pdf : we will be use PypdfLoader for this type of pdf 
2) PDF with tabular data (table row , columns data):  we will use for this PdfPlumberLoader for this type of pdf
3)  PDF with basic image layout: we wiil use for this PyMUPDFLoader for this type of pdf
4) PDF with complete scanned images: we will use for this UnstructuredPDFLoader or AmazonTExtractPDFLoader for this type of pdf


DirectoryLoader: Directory loader is a document loader that loads multiple documnent from the directory folder. Directory loads the file content or files as per the pattern followed by these files.

Glob Pattern 


EnterPrise Level RAG Application ()


Difference between load() and lazyload()
load(): This helps in eager loading as loading everything at once and return a list of documents object
All data is loaded directly into the memory 
The number of documents then we should use this type of load() function
You want everything loaded infront of memory.



Lazyload(): It goes with lazy-loading and loads on demands.
It return a generator of Document Objects
Documents are not loaded at once then are fetched once at a time as needed. 
Used for large documents or lots of file 
You want to stream processing (chunks , embedding ) without using the lots of memory
