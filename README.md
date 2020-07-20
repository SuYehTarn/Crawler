# Crawler
> A crawler for static web page

**Crawler** is a simple crawler for Python.

## Installation

OS X & Linux:

Download Python 3 from [Python.org](https://www.python.org/downloads/) and install it.

Download **Crawler** and place it at arbitrary direction.

Windows:

Download Python 3 from [Python.org](https://www.python.org/downloads/) and install it.

Download **Crawler** and place it at arbitrary direction.

## Usage example

User would have to edit the file `main.py` and run **Crawler** with it. User has three things to decide. The first is the working list. The second is the **UrlMatcher**. The Third is the **Extractors**. After setting three of them, the crawler may crawl.

### Define the Working List

The **Crawler** object has a **WorkingListManager** controling the working list for the **Crawler**. When initialize the **Crawler**, we set a list contains at least one work as the working list. For example:

	args = {
	    ...
	    'workingList': ['http://www.firstpage.com']
	    ...
	}
	c = Crawler(**args)

In the example, we set `http://www.firstpage.com` as an element of the working list. It would be treated as the first web page url to crawl.

Setting working list, user can arrange the works before the crawler starts. Multiple works are allowed.

### Define the UrlMatcher

Automatically adding urls into the working list might meets the need of user. There are four arguments of **Crawler** initializing relative to this issue: `scheme_pattern`, `domain_pattern`, `path_pattern`, and `autoAddInternalLinks`. 

* `scheme_pattern`: The regex of the url scheme. `r'http|https'` is set default, means the url having `http` or `https` would be regarded as included.
* `domain_pattern`: The regex of the url domain. `r'.*'` is set default, means the url having any domain would be regarded as included.
* `path_pattern`: The regex of the path domain. `r'.*'` is set default, means the url having any path of domain would be regarded as included. If it is specified, it must start with `'/'`.
* `autoAddInternalLinks`: The boolean value handle the automatically adding url. If it set `True`, when crawling a web page, all urls found on the web page and regarded as included with the `scheme_pattern`, `domain_pattern`, and `path_pattern` would add into the working list. `True` is set default.

For example:

	args = {
		...
	    'scheme_pattern': r'https',
	    'domain_pattern': r'www.domain.com',
	    'path_pattern': r'/blog',
	    'autoAddInternalLinks': True,
	    ...
	}
	c = Crawler(**args)

In the example, the **Crawler** would automatically add urls into its working list. The url must have a scheme of `https`, a domain of `www.domain.com`, and a path of `/blog`.

### Define the Extractors

If user would like to collect data during crawling, extractors must be defined. User defines a new object inheriting the **Extractor** imported from the module `Extractor`. The user defined extractor have some method of extracting data with the url and the BeautifulSoup object ([know more](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)) of a web page. An extracting method has a name in the format of `get_{attribute name}`. The attribute name would be the key to save the data into an object in a `.json` file. An extracting method must have two returning object. The first is the data attempted to collect. In order to save it into a `.json` file, following data types are recommanded: dict, list, tuple, str, int, float, bool, type(None). Data of other types would be saved as its string representation. The second is the additional message returned from the extractor. It can be remained as an empty string, the extractor would still returns the information about the succesfulness of the extracting method. Here is an example in `main.py`:

	class Title(Extractor):

	    def get_url(self, url, bs):
	        data = url
	        msg  = ''
	        return data, msg

	    def get_title(self, url, bs):
	        data = bs.head
	        data = data.title.get_text()
	        msg = ''
	        return data, msg

In this example, the user defined an extractor `Title`. `Title` has two extracting method: `get_url` and `get_title`. `get_url` simply returns the input url. `get_title` extract the text of the tag `<title>`  under the tag `<head>`. These method do not returns any additional message.

User can ignore the control of exceptions. It would be handle by a decorator of the **Extractor**.

## Release History

* 0.1.0
	* The first proper release

## Meta

Su, Yeh-Tarn - nukdus@msn.com

[https://github.com/nucklus](https://github.com/nucklus)