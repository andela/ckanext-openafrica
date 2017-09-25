openAFRICA CKAN Extension
=========================

Website: [openAFRICA](http://openAFRICA.net)
Latest Version: 1.0.0

Currently on customises the look and feel in very basic ways.

Use http://docs.ckan.org/en/latest/contents.html to set up CKAN

Then


Enabling View Counts
====================
Please read [Page View Tracking](http://docs.ckan.org/en/latest/maintaining/tracking.html?highlight=tracking) first, if you want to enable view counts on datasets and resources.
View counts can be enabled to display how many times a package or resource has been viewed. 
To enable view count, you have to add the following to your config file (e.g production.ini):
```
  show_view_count=true

  admin_api_key=your-api-key
```

You can see your API key by visiting ``/user/your-user-name``. It is located in the user details by the left.
Using a wrong API key may result to an internal server error or 403 error.
