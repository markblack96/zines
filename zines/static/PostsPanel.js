
class PostsPanel extends HTMLElement {
    constructor() {
        super()
        let template = document.querySelector('#posts-panel');
        let content = template.content;
        const shadowRoot = this.attachShadow({mode: 'open'}).appendChild(content.cloneNode(true));

        this._posts = [];
    }
    static get observedAttributes() {
        return ['posts']
    }
    attributeChangedCallback(name, oldValue, newValue) {
        console.log("newValue", newValue);
    }
    connectedCallback() {
        fetch('/posts')
            .then(resp=>resp.json())
            .then(data=>{
                console.log("Data from connectedCallback()", data);
                this.posts = data;
                // this.setAttribute('posts', data)
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
        let postDivs = this.posts.map(post=>{
            let container = document.createElement('div');
            let titleSpan = document.createElement('span');
            titleSpan.innerText = `${post.title}`;
            let deleteButton = new FetchEnabledButton();

            container.appendChild(titleSpan);
            container.appendChild(deleteButton);            
            this.shadowRoot.appendChild(container);
        })
        return postDivs
    }
}
customElements.define('posts-panel', PostsPanel)