# LinkDumper Burp Plugin

> Tab view panel using `IMessageEditorTab` to dump all the links from the responses:

![LinkDumper](https://user-images.githubusercontent.com/13177578/63759484-39863300-c8db-11e9-9090-5cd52ae6fffd.PNG)
 
# Workflow:

> Dump links from respones,If url is hex/url encoded then decode it,Sort all the results to put the most likeable links at the top & rest junk(html/javascript junk) in the last.

 > Why to include junk? why not just links:
* Finding all possible type links is really difficult task,There are many cases where the endpoints are stored in differential structures where they are hard to extract using regex.
* So it's a good practice a take a look around junks to find something interesting.

# Customize:

> Dump links from the responses of content-types defined at `WHITELIST_MEMES ` list. Modify it accordingly, The more you keep it accurate the less memory it takes.




