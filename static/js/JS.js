const URL='http://192.168.0.148:3000/';


async function loadComments(id){
    let comment_block=document.getElementById(`comments_${id}`);
    // comment_block.innerText=comment_block.innerText+`<div class="collapse" id="comments_${id}">`;
    await fetch(`https://jsonplaceholder.typicode.com/comments?postId=${id}`)
        .then(response=>response.json())
        .then(comments=>{

            for(let i=0;i<comments.length;i++){
                let user_name = comments[i].name+` (${comments[i].email})`;
                let text = comments[i].body;


                // comment_block.innerText=comment_block.innerText+`<div class="card card-body">${text}</div>`;
                //console.log(comment_block.innerText);


                let Comment=document.createElement(`div`);
                let comTitle=document.createElement('h5');
                let comBody=document.createElement('p');
                let comUser=document.createElement('p');
                let comEmail=document.createElement('a');


                comUser.textContent=comments[i].name;
                comUser.classList.add('d-inline');
                comUser.classList.add('p-2');

                comEmail.href=`mailto:${comments[i].email}`;
                comEmail.textContent=`(${comments[i].email})`;
                comEmail.classList.add('d-inline');

                comTitle.classList.add('card-title');
                comTitle.appendChild(comUser);
                comTitle.appendChild(comEmail);

                comBody.classList.add('card-text');
                comBody.textContent=text;

                Comment.classList.add('card');
                Comment.classList.add('card-body');
                Comment.classList.add('bg-light');
                Comment.classList.add('mb-1');
                Comment.appendChild(comTitle);
                Comment.appendChild(comBody);


                if(i==0){
                    removeLoadIcon()
                }
                comment_block.appendChild(Comment);
            }
        });
}

async function doneTask(id){
    await fetch(`${URL}condition/${id}`,{
        method: 'GET',
        headers:{
            'Content-Type': 'application/json',
        },
    }).then(()=>{
        let button=document.getElementById(`done_button_${id}`);
        let title = document.getElementById(`task_title_${id}`);
        let description = document.getElementById(`task_description_${id}`);
        let linkTitle=document.getElementById(`task_title_${id}`);
        let textDescription=document.getElementById(`task_description_${id}`);
        if(button.classList.contains('btn-outline-secondary')){
            let title_text=title.innerHTML;
            let description_text=description.innerHTML;
            title.innerHTML=`<del id='del_title_${id}'>${title_text}</del>`;
            description.innerHTML=`<del id='del_descr_${id}'>${description_text}</del>`;
            button.classList.remove('btn-outline-secondary');
            button.classList.add('btn-secondary');
            linkTitle.classList.add('disabled');
            textDescription.classList.add('text-secondary');
            let checkbox=document.getElementById('onlyDone');
            if (checkbox.checked){
                let task=document.getElementById(`card_${id}`);
                task.remove();
            }
        }else{
            let titleDel = document.getElementById(`del_title_${id}`).innerHTML;
            let descriptionDel = document.getElementById(`del_descr_${id}`).innerHTML;
            title.innerHTML=titleDel;
            description.innerHTML=descriptionDel;
            button.classList.remove('btn-secondary');
            button.classList.add('btn-outline-secondary');
            linkTitle.classList.remove('disabled');
            textDescription.classList.remove('text-secondary');
        }
    });
}

async function removeTask(id){
    await fetch(`${URL}delete/${id}`,{
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    }).then(()=>{
        document.getElementById(`card_${id}`).remove();
    });
}

async function removeLoadIcon(){
    document.getElementById('spinner_loading').remove();
}

//Показать и скрыть выполненные задачи
async function transformTaskList(){
    let checkbox=document.getElementById('onlyDone');
    if(checkbox.checked){
        let allTasks=document.getElementsByClassName('card');
        for(let i=0;i<allTasks.length;i++){
            if(Done(allTasks[i])){
                allTasks[i].remove();
                i--;
            }
        }
    }
    else{
        await fetch(`${URL}tasks`,{
        method: 'GET',
        headers:{
            'Content-Type': 'application/json',
        },})
        .then(response=>response.text())
        .then(comments=>{
            let parser=new DOMParser();
            let page=parser.parseFromString(comments,'text/html');
            let oTask=document.getElementById('accordionExample');
            let loading=page.getElementsByClassName('spinner-border');
            while(loading[0]){
                loading[0].remove();
            }
            oTask.innerHTML=page.getElementById('accordionExample').innerHTML;
        });
    }
}

function Done(task){
    let find=task.children[1];
    while(find.children[0]){
        find=find.children[0];
    }
    if (find.tagName=='DEL'){
        return true;
    }
    return false;
}


async function FilterByName(){
    let filterName=document.getElementById('filterName').value.toLowerCase();
    if (filterName.trim()!=""){

        await fetch(`${URL}tasks`,{
        method: 'GET',
        headers:{
            'Content-Type': 'application/json',
        },})
        .then(response=>response.text())
        .then(comments=>{
            let htmlParser=new DOMParser();
            let htmlPage=htmlParser.parseFromString(comments,'text/html');
            let tasksOld=document.getElementById('accordionExample');
            let loading=htmlPage.getElementsByClassName('spinner-border');
            while(loading[0]){
                loading[0].remove();
            }
            tasksOld.innerHTML=htmlPage.getElementById('accordionExample').innerHTML;
        });

        let cards=document.getElementsByClassName('card');
        for (let i=0;i<cards.length;i++){
            let titleFirst=cards[i].children[1];
            while (titleFirst.children[0]){
                titleFirst=titleFirst.children[0];
            }
            let titleTask=titleFirst.textContent.toLowerCase();
            if (titleTask!=filterName){
                cards[i].remove();
                i--;
            }
        }
    }
    else
    {
        await fetch(`${URL}tasks`,{
        method: 'GET',
        headers:{
            'Content-Type': 'application/json',
        },})
        .then(response=>response.text())
        .then(comments=>{
            let htmlParser=new DOMParser();
            let htmlPage=htmlParser.parseFromString(comments,'text/html');
            let tasksOld=document.getElementById('accordionExample');
            let loading=htmlPage.getElementsByClassName('spinner-border');
            while(loading[0]){
                loading[0].remove();
            }
            tasksOld.innerHTML=htmlPage.getElementById('accordionExample').innerHTML;
        });
    }
}