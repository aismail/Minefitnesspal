var request = require("request");
var _ = require("underscore");
var FB = require('fb');
var fs = require('fs');

FB.setAccessToken('1543530219228022|l2ghob0T2nzJOYeiCvm2XlX--ws');
var NUM_POSTS = 1000;
if (process.argv.length !=3) {
    console.log("You must give a valid Facebook Page ID as an additional argument and nothing else.")
    return;
}

var fbid = process.argv[2];
var url = 'https://graph.facebook.com/v2.2/' + fbid + '/posts?access_token=1543530219228022|l2ghob0T2nzJOYeiCvm2XlX--ws';
var urlForValidFBRequest = 'https://graph.facebook.com/v2.2/' + fbid + '?access_token=1543530219228022|l2ghob0T2nzJOYeiCvm2XlX--ws';
var NUM_CHARS_UNTIL_NEXT_PAGE_ROUTE = "https://graph.facebook.com/v2.2".length;
var OUTPUT_FILE = "data.txt";

var getPosts = function(posts,url,depth){
    console.log("depth: " + depth);
    if (Object.keys(posts).length>NUM_POSTS) {
        return fs.writeFile(OUTPUT_FILE,JSON.stringify(posts), function (err) {
              if (err) throw err;
              console.log('It\'s written in data.txt.');
              return JSON.stringify(posts);
        });
    }

    request.get(url, function (req,res) {
        res = JSON.parse(res.body);
        if (!res || res.error) {
            console.log(!res ? 'error occurred' : res.error);
            return fs.writeFile(OUTPUT_FILE,JSON.stringify(posts), function (err) {
              if (err) throw err;
              console.log('It\'s written in data.txt, despite the error.');
              return JSON.stringify(posts);
            });
        }
        _.each(res.data,function(v){
            if (!v.likes || !v.comments || !v.message || !v.shares) {
                return;
            }
            var post = {};
            post['message'] = v.message;
            post['numLik'] = v.likes.data.length;
            post['numCom'] = v.comments.data.length;
            post['numShares'] = v.shares.count;
            posts[v.id] = post;
        });
        if (! res.paging) {
        	console.log("There are less than " + NUM_POSTS + " posts by the target Facebook page.")
        	return fs.writeFile(OUTPUT_FILE,JSON.stringify(posts), function (err) {
              if (err) throw err;
              console.log('It\'s written in data.txt.');
              return JSON.stringify(posts);
       		});
        }
        url = res.paging.next;
        return getPosts(posts,url,depth+1);
    });
}

request.get(urlForValidFBRequest,function(req,res){
    if (!res || res.error) {
        console.log("Not a valid Facebook Page ID");
    }
    else {
        //schema of post
        //id,message,numLik,numCom, numShares
        var posts = {};
        var x = getPosts(posts,url,0);
    }
});

