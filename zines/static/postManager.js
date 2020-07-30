// display post info with options
const postManager = {
    label: 'Posts',
    posts: fetch('/posts')
                .then(response => response.json())
                .then(data => data),
    options: (post) => [
        {
            label: 'Edit', 
            link: `/write/${post.post_id}`, 
            method: 'GET', 
            make: function() {
                let anchor = document.createElement('a');
                anchor.innerText = this.label;
                anchor.href = this.link;
                return anchor;
            }
        },
        {
            label: 'Edit Header Image',
            link: `/edit/image/${post.post_id}`,
            method: 'GET',
            make: function() {
                let anchor = document.createElement('a');
                anchor.innerText = this.label;
                anchor.href = this.link;
                return anchor;
            }
        },
        {
            label: 'Toggle Hide', 
            link: `/hide/${post.post_id}`, 
            method: 'PATCH', 
            make: function() {
                let btn = document.createElement('button')
                btn.innerText = this.label;
                btn.onclick = () => {
                    fetch(this.link, {'method': 'PATCH', headers: {'X-CSRFToken': document.querySelector('meta[name=csrf-token]').content}}).then(response=>response.json())
                    .then(
                        (d)=>{
                            console.log(d);
                            btn.parentElement.parentElement.firstChild.innerHTML = `${d.title} ${d.hidden ? '<span style="color: red">(Hidden)</span>' : ''}`;
                            // the above code is a monstrosity and needs to be fixed with proper web components and state management eventually
                        }
                    );
                }
                return btn;
            }
        },
        {
            label: 'Delete',
            link: `/delete/${post.post_id}`,
            method: 'DELETE',
            make: function() {
                let btn = document.createElement('button');
                btn.innerText = this.label;
                btn.onclick = () => {
                    fetch(this.link, {'method': 'DELETE', headers: {'X-CSRFToken': document.querySelector('meta[name=csrf-token]').content}}).then(response=>response)
                    .then((d)=>{
                        if (d.status == 200) {
                            alert('Post deleted.');
                            // update table / remove this post from table
                            let table = btn.parentElement.parentElement.parentElement;
                            table.removeChild(btn.parentElement.parentElement)
                        }
                        console.log(d);
                    })
                    .catch(error=>console.error('Error: '+ error))
                }
                return btn;
            }
        }
    ],
    make: function(element) {
        // collect posts and display them
        var options = this.options;
        // notify user posts are being fetched
        const panel = element;
        panel.innerText = 'Loading posts, please wait';
        this.posts.then((data)=>{
            let panel = element;
            let table = document.createElement('table');
            for (i = 0; i < data.length; i ++) {
                let post = data[i];
                let row = document.createElement('tr');
                let title = document.createElement('td');
                console.log(post.hidden);
                title.innerHTML = `${post.title} ${post.hidden === true ? '<span style="color: red">(Hidden)</span>' : ''}`;
                row.appendChild(title);
                options(post).forEach((d)=>{
                    let opt = d.make();
                    let td = document.createElement('td');
                    td.appendChild(opt);
                    row.appendChild(td);
                });
                table.appendChild(row);
            }
            panel.innerText = ''; // remove notification
            return table;
        }).then((table)=>element.appendChild(table));

    /* 
     * originally I attempted to abuse template literals to do the above. I am putting
     * a note to myself here not to attempt to do so again.
     */

    }
    
}