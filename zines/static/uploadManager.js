/* admin panel upload manager */

const uploadManager = {
    label: 'Upload',
    options: [
        {label: 'Upload Markdown', link: ''}, {label: 'Upload Image', link: ''}
    ],
    make: function(element) {
        let panel = document.createElement('div');
        this.options.forEach((o)=>{
            let input = document.createElement('input');
            input.type = 'file';
            let inputLabel = document.createElement('label');
            inputLabel.innerText = o.label;
            inputLabel.appendChild(input);
            let button = document.createElement('button');
            button.innerText = 'Upload';
            button.onclick = () => {
                button.disabled = true;
                fetch(this.link, 
                    {  
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: 
                    }
                )
                .then(d=>d.json())
                .then((d)=>{

                })
            }
            panel.appendChild(inputLabel);
            
        })
        element.appendChild(panel);
    }
}