document.addEventListener('DOMContentLoaded', function() {
  
    // Use buttons to toggle between views
    document.querySelector('form').onsubmit = post_form;
    
    document.querySelector('#allposts').addEventListener('click',load_all_messages );
    document.querySelector('#home').addEventListener('click',load_message );
    /*  document.querySelectorAll('.profile').forEach(div => {
      div.addEventListener('click', () => {
          view_profile();
        });
      });*/
    //load_message();
    /*document.querySelectorAll('button').forEach(button =>{
        button.onclick = function(){
            document.querySelector('btn').style.color=button.dataset.color;
        }
    })*/

   
    

    
});
    var count =0;


    function changeColor(x){
        var x;
        if(x==1){
            count=count+1;
        }
        
        if(count == 1){
            document.getElementById('btn').style.background="blue";
            document.getElementById('btn').style.color="white";
        }
        else if(count == 2){
            document.getElementById('btn').style.background="";
            document.getElementById('btn').style.color="blue";
            count =0;
        }
            

        }

        

    function like(post_id){
                console.log(post_id);
                var url = '/like/'+post_id;
                console.log(url);
                fetch(url, {
                    method: 'POST',
                    body: JSON.stringify({
                        id: post_id
                    })
                })
                .then(response => response.json())
                .then(data => {
                 
                    
                    console.log(total_likes);

                    if(data.liked==='t'){
                        document.getElementById(post_id).innerHTML= "Unlike";
                        //document.getElementById("totallikes"+post_id).innerHTML= total_likes_number+1;
                        var total_likes=document.getElementById("totallikes"+post_id);
                        total_likes_number = parseFloat(total_likes.innerHTML);
                        total_likes_number++;
                        total_likes.innerHTML = total_likes_number;

                      }
                    if(data.liked==='f'){
                        document.getElementById(post_id).innerHTML= "Like"; 
                        //document.getElementById("totallikes"+post_id).innerHTML= total_likes_number-1;
                        var total_likes=document.getElementById("totallikes"+post_id);
                        total_likes_number = parseFloat(total_likes.innerHTML);
                        total_likes_number--;
                        total_likes.innerHTML = total_likes_number;
                      }
                    
                })
           

    }

    function follows(owners_id){


        console.log(owners_id);
        var url = '/followers_count/'+owners_id.slice(1);
        console.log(url);
        fetch(url, {
            method: 'POST',
            body: JSON.stringify({
                id: owners_id.slice(1)
            })
        })
        .then(response => response.json())
        .then(data => {
         
            console.log(data.follows);
            console.log(data.total_follows);
            
            if(data.follows==='t'){
                document.getElementById(owners_id).innerHTML= "Unfollow";
                //document.getElementById("totallikes"+post_id).innerHTML= total_likes_number+1;
                var total_follows=document.getElementById("profile-stat-count");
                total_follows_number = parseFloat(total_follows.innerHTML);
                total_follows_number++;
                total_follows.innerHTML = total_follows_number.toString();

              }
            if(data.follows==='f'){
                document.getElementById(owners_id).innerHTML= "Follow"; 
                //document.getElementById("totallikes"+post_id).innerHTML= total_likes_number-1;
                var total_follows=document.getElementById("profile-stat-count");
                total_follows_number = parseFloat(total_follows.innerHTML);
                total_follows_number--;
                total_follows.innerHTML = total_follows_number.toString();
              }
            
        })
   

}
  
    function hello(){
        alert('Hello,world!');
        console.log("hello");
    }

    function load_message(){
        document.querySelector('#all_posts').style.display = 'block';
        document.querySelector('#all_messages').style.display = 'none';

       // console.log();
        console.log("hello world");

        fetch('/get_message')
        .then(response => response.json())
        .then(result =>{
            console.log("bhobho");
            console.log(result);
            appendData(result);

            //document.querySelector('#test2').innerHTML = result.user_id.username;
        })
        
        return false;
    }

    function load_all_messages(){
        document.querySelector('#all_posts').style.display = 'none';
        document.querySelector('#all_messages').style.display = 'block';
        //document.querySelector('#all_posts').innerHTML = `today`+ post;

       // console.log();
        console.log("hello world");

        fetch('/get_all_messages')
        .then(response => response.json())
        .then(result =>{
            console.log("kae");
            console.log(result);
            appendMessages(result);
        })
        
        return false;
    }
    function appendData(result){
        var mainContainer = document.getElementById("all_posts");
        mainContainer.innerHTML="";
        for (var i = 0; i < result.length; i++) {
            // append each person to our page
            var div = document.createElement("div");
            var c_id=String(i);
            div.setAttribute("id",c_id);
            div.setAttribute("class","profile")
            div.addEventListener('click',view_profile(result[i].user_id));
            div.innerHTML = result[i].user_id + result[i].user + result[i].message + result[i].timestamp  ;



            var button = document.createElement("button");
            button.innerHTML = "like";
            button.onclick = function(){
            alert('here be dragons');return false;
            };
           /* var btn_follow = document.createElement("button");
            btn_follow.innerHTML="follow";
            btn_follow.setAttribute("style","margin-left:40px")
            btn_follow.onclick= function(){
            alert('Follow me');return false;
            };
            */
            mainContainer.appendChild(div);
            mainContainer.appendChild(button);
            //mainContainer.appendChild(btn_follow);
          }

    }
    function appendMessages(result){
        var mainContainer = document.getElementById("all_messages");
        mainContainer.innerHTML="";

        for (var i = 0; i < result.length; i++) {
            // append each person to our page
            var div = document.createElement("div");
            div.setAttribute("id",result[i].id);
            div.setAttribute("class","profile")

            div.innerHTML = result[i].user + result[i].message + result[i].timestamp ;
            
            div.addEventListener('click',view_profile(result[i].user_id));

            //var button = document.createElement("button");
            //button.innerHTML = "like";
            //button.onclick = function(){
            //alert('here be dragons');return false;
            //};
            /*var btn_follow = document.createElement("button");
            btn_follow.innerHTML="follow";
            btn_follow.setAttribute("style","margin-left:40px")
            btn_follow.onclick= function(){
            alert('Follow me');return false;
            };*/
            
            mainContainer.appendChild(div);
            mainContainer.appendChild(button);
            //mainContainer.appendChild(btn_follow);
          }

    }

    function post_form(){
        const p = document.querySelector('#post').value;
        console.log(p);
        console.log("-----");
        fetch('/add_post',{
            method: 'POST',
        //   credentials: "same-origin",
        //   headers: {'X-CSRFToken': csrftoken},
            body: JSON.stringify({
               
                message: p,

          })
        })
        .then(response => response.json())
        .then(result =>{
            console.log(result);
            console.log("-----");
            document.querySelector('#post').value="";
            appendData(result);
            //document.querySelector('#sender').innerHTML = result.user_id;
        })
        .catch(error => {
            console.log('Error',console.error);
        });
        
        return false;
    }

    
    function edit(id) {
        var edit_box = document.querySelector(`#edit-box-${id}`);
        var edit_btn = document.querySelector(`#edit-btn-${id}`);
        var post = document.querySelector(`#post-${id}`);
        edit_box.style.display = 'block';
        edit_btn.style.display = 'block';
        post.style.display= 'none';
    
        edit_btn.addEventListener('click', () => {
            fetch('/edit/' + id, {
                method: 'PUT',
                body: JSON.stringify({
                    post: edit_box.value
                })
              });
            
              edit_box.style.display = 'none';
              edit_btn.style.display = 'none';
              post.style.display= 'block';
              
              document.querySelector(`#post-${id}`).innerHTML = edit_box.value;
        });
    
        edit_box.value = document.querySelector(`#post-${id}`).innerHTML;
    }

   /* function like(){
        var button = document.createElement('button');
        button.innerHTML = 'like';
        button.onclick = function(){
          alert('here be dragons');return false;
        };
        // where do we want to have the button to appear?
        // you can append it to another element just by doing something like
        // document.getElementById('foobutton').appendChild(button);
        document.getElementById('all_messages').appendChild(button); 
        document.body.appendChild(button);
      }; */

    function view_profile(user_id){
        console.log(user_id);
        var url = '/profile/'+user_id;
        console.log(url);
        fetch(url)
        .then(response => response.json())
        .then(result =>{
            console.log("profile");
            console.log(result);
           //hide other divs
           // display profile div
    }); 
   }
