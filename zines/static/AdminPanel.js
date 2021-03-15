class extends HTMLElement {
    constructor(panels) {
        super()
        let template = document.querySelector('#admin-panel');
        let content = template.content;
        const shadowRoot = this.attachShadow({mode: 'open'}).appendChild(content.cloneNode(true));
        this._panels = []
    }
    connectedCallback() {

    }
}