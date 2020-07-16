const imageManager = {
    images: fetch('/images').then(response => response.json()).then(data => data),
    options: [],
    make: function() {
        let imagePanel = document.querySelector('#imagePanel');
        this.images.then(data=>console.log(data));
        this.images.then(data=>{
            for (let i = 0; i < data.length; i++) {
                let row = document.createElement('tr');
                let thumbNailCell = document.createElement('td');
                let thumbnail = document.createElement('img');
                thumbnail.src = data[i].url;
                thumbNailCell.appendChild(thumbnail);
                row.appendChild(thumbNailCell);
                console.log(row.innerHTML);
            }
        })
    }
}