import FetchEnabledButton from './DeleteButton.js'
import EventBus from './EventBus.js'

class PostsPanel extends HTMLElement {
    constructor() {
        super()
        let template = document.querySelector('#posts-panel');
        let content = template.content;
        const shadowRoot = this.attachShadow({mode: 'open'}).appendChild(content.cloneNode(true));

        this._posts = [];
        console.log("this", this)
        
        EventBus.register('fetch-button-clicked', async (e)=>{
            console.log('click')
            await this._getPosts()
                .then(posts=>{
                    this.posts = posts;
                })
        })
    }
    static get observedAttributes() {
        return ['posts']
    }
    attributeChangedCallback(name, oldValue, newValue) {
        console.log("newValue", newValue);
    }
    async _getPosts() {
        return await fetch('/posts')
            .then(resp=>resp.json())
    }
    connectedCallback() {
        this._getPosts()
            .then(posts=>{
                this.posts = posts
            })
    }
    get posts() {
        return this._posts
    }
    set posts(posts) {
        this._posts = posts
        this.render()
    }
    render() {
        console.log("Posts from render()", this.posts)
        this.shadowRoot.querySelector('#posts-panel').innerHTML = '';
        let postDivs = this.posts.map(post=>{
            let container = document.createElement('div');
            let titleSpan = document.createElement('span');
            titleSpan.innerText = `${post.title}`;
            let deleteButton = new FetchEnabledButton(`/delete/${post.post_id}`, {method: 'DELETE', headers: {'X-CSRFToken': document.querySelector('meta[name=csrf-token]').content}});

            container.appendChild(titleSpan);
            container.appendChild(deleteButton);            
            this.shadowRoot.querySelector('#posts-panel').appendChild(container);
        })
        return postDivs
    }
}
customElements.define('posts-panel', PostsPanel)