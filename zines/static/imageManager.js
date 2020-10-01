const imageManager = {
    label: 'Images',
    images: fetch('/images').then(response => response.json()).then(data => data),
    options: (image, row)=>[
        {
            label: 'Delete',
            link: `/images/${image.id}/delete`, 
            method: 'DELETE', 
            parent: row,
            make: function() {
                let button = document.createElement('button');
                button.innerText = this.label;
                button.onclick = () => {
                    fetch(this.link, {'method': this.method, headers: {'X-CSRFToken': document.querySelector('meta[name=csrf-token]').content}})
                        .then(d=>d.json())
                        .then(this.parent.remove())
                        .then(d=>alert(d.message));
                }
                return button;
            }
        }
    ],
    make: function(element) {
        this.parent = element; // set parent element
        this.images.then(data=>console.log(data));
        this.images.then((data) => {
            let table = document.createElement('table');
            for (let i = 0; i < data.length; i++) {
                let row = document.createElement('tr');
                let thumbNailCell = document.createElement('td');
                let thumbnail = document.createElement('img');
                thumbnail.src = 'uploads/' + data[i].url; // todo: maybe don't hardcode this
                thumbnail.style.maxWidth = '100px';
                thumbNailCell.appendChild(thumbnail);
                row.appendChild(thumbNailCell);
                let label = document.createElement('span');
                label.innerText = data[i].url;
                row.appendChild(label);
                row.style.display = 'flex';
                row.style.alignItems = 'center';
                this.options(data[i], row).forEach((d)=>{
                    let opt = d.make();
                    let td = document.createElement('td');
                    td.appendChild(opt);
                    row.appendChild(td);
                    console.log(opt);
                });
                table.appendChild(row);
            }
            element.appendChild(table);
        });
    }
}