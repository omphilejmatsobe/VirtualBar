const cardData = [
    {
        name:"",
        descition:"",
        Time:"",
        Type:"",
    }
]

const card = document.querySelector('call-logs');

const cardArray = () =>{
    cardData.map((obj)=>{
        const post = document.createElement('div');
        post.classList.add('call-history');
        post.innerHTML=`

        <div class="card-top">
        <!-- This is where name goes -->
        <div class="top-left">
            <h1>${obj.name}</h1>
            <h3>${obj.descition}</h3>
        </div>
        <div class="top-right">
            <div>
                <div class="delete"><img class="add-delete" src="/static/images/delete.png"/></div>
            </div>
        </div>
    </div>
    <div class="card-bottom" >
        <div><h1>${obj.Time}</h1></div>
        <div><h1>${obj.Type}</h1></div>
    </div>
        `

        card.appendChild(post);
    })
}
