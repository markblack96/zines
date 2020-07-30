/* admin panel upload manager */

const uploadManager = {
    label: 'Upload',
    options: [
        {label: 'Upload Markdown', link: '/upload/md', id: 'markdown'}, {label: 'Upload Image', link: '/upload/image', id: 'image'}
    ],
    make: function(element) {
        let panel = document.createElement('div');
        this.options.forEach((o)=>{
            let input = document.createElement('input');
            input.type = 'file';
            input.id = o.id;
            input.name = 'file';
            let inputLabel = document.createElement('label');
            inputLabel.innerText = o.label;
            inputLabel.appendChild(input);
            let button = document.createElement('button');
            button.innerText = 'Upload';
            button.onclick = () => {
                let file = document.querySelector('#'+o.id).files[0];
                console.log(file);
                let data = new FormData();
                data.append('file', file);
                button.disabled = true;
                fetch(o.link, 
                    {  
                        'method': 'POST',
                        'body': file,
                        headers: {'Content-Type': 'application/json', 'X-CSRFToken': document.querySelector('meta[name=csrf-token]').content}
                    }
                )
                .then(d=>d.json())
                .then((d)=>{
                    alert(d.message);
                })
                .catch((d)=>console.log);
            }
            panel.appendChild(inputLabel);
            panel.appendChild(button);
            
        })
        element.appendChild(panel);
    }
}