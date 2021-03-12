/**
 * A custom button element that takes a URL and 
 * @params url
 */

 class FetchEnabledButton extends HTMLButtonElement {
    constructor(url, options) {
        super()
        this._url = url
        this._options = options
        this.innerText = 'Delete'
    }
    static get observedAttributes() {
        return ['url']
    }
    attributeChangedCallback(name, oldValue, newValue) {
        console.log("newValue", newValue);
    }
    connectedCallback() {
        this.url = '/some-endpoint'
        this.onclick = this.onClick;
    }
    get url() {
        return this._url
    }
    set url(url) {
        this._url = url
    }
    onClick(e) {
        console.log(e)
        console.log(this.url)
        fetch(this.url, this._options)
            .then(resp=>resp.json())
            .then(console.log)
            .catch(err=>console.log(err))

    }
}
customElements.define('fetch-button', FetchEnabledButton, {extends: 'button'})