var request = require("request");
var _ = require("underscore");
var FB = require('fb');

FB.setAccessToken('1543530219228022|l2ghob0T2nzJOYeiCvm2XlX--ws');

//schema of post
//id,message,numLik,numCom

var posts = {};
var url = 'https://graph.facebook.com/v2.2/myfitnesspal/posts?access_token=1543530219228022|l2ghob0T2nzJOYeiCvm2XlX--ws';
var NUM_CHARS_UNTIL_NEXT_PAGE_ROUTE = "https://graph.facebook.com/v2.2".length;



// request.get("https://graph.facebook.com/v2.2/myfitnesspal/posts?access_token=1543530219228022|l2ghob0T2nzJOYeiCvm2XlX--ws", function(req,res){
//     console.log(typeof(res));
// })
var getPosts = function(posts,url,depth){
    console.log("depth: " + depth);
    if (Object.keys(posts).length>500) {
        console.log(JSON.stringify(posts));
        return posts;
    }
    
    request.get(url, function (req,res) {
        res = JSON.parse(res.body);
        if(!res || res.error) {
            console.log(!res ? 'error occurred' : res.error);
            console.log(posts)
            return;
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
        url = res.paging.next;
        getPosts(posts,url,depth+1);
    });
}
var x = getPosts(posts,url,0)

