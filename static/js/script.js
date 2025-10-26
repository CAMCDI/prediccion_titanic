document.getElementById('predictionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const submitBtn = document.querySelector('.submit-btn');
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoading = submitBtn.querySelector('.btn-loading');
    
    btnText.style.display = 'none';
    btnLoading.style.display = 'block';
    submitBtn.disabled = true;
    
    
    const formData = {
        Pclass: parseInt(document.getElementById('Pclass').value),
        Sex: document.getElementById('Sex').value,
        Age: parseInt(document.getElementById('Age').value),
        SibSp: parseInt(document.getElementById('SibSp').value),
        Parch: parseInt(document.getElementById('Parch').value),
        Embarked: document.getElementById('Embarked').value,
        Title: document.getElementById('Title').value
    };
    
    try {
        const response = await fetch('/predict/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Error en la predicción');
        }
        
        
        showResult(data.prediction);
        
    } catch (error) {
        alert(' Error: ' + error.message);
    } finally {
        
        btnText.style.display = 'block';
        btnLoading.style.display = 'none';
        submitBtn.disabled = false;
    }
});

function showResult(prediction) {
    const resultDiv = document.getElementById('result');
    const predictionText = document.getElementById('predictionText');
    
   
    if (prediction.includes('Sobrevive')) {
        predictionText.innerHTML = ' ' + prediction;
        predictionText.style.color = '#2e7d32';
        predictionText.style.background = 'rgba(165, 214, 167, 0.3)';
        predictionText.style.borderColor = '#a5d6a7';
    } else {
        predictionText.innerHTML = ' ' + prediction;
        predictionText.style.color = '#c62828';
        predictionText.style.background = 'rgba(239, 154, 154, 0.3)';
        predictionText.style.borderColor = '#ef9a9a';
    }
    
    resultDiv.style.display = 'block';
    resultDiv.scrollIntoView({ behavior: 'smooth' });
}

function resetForm() {
    document.getElementById('predictionForm').reset();
    document.getElementById('result').style.display = 'none';
    
   
    window.scrollTo({ top: 0, behavior: 'smooth' });
}


document.querySelectorAll('input, select').forEach(element => {
    element.addEventListener('focus', function() {
        this.parentElement.style.transform = 'translateY(-5px)';
    });
    
    element.addEventListener('blur', function() {
        this.parentElement.style.transform = 'translateY(0)';
    });
});


function createParticle() {
    const particle = document.createElement('div');
    particle.style.cssText = `
        position: fixed;
        width: 4px;
        height: 4px;
        background: rgba(149, 117, 205, 0.3);
        border-radius: 50%;
        pointer-events: none;
        z-index: 1;
    `;
    document.body.appendChild(particle);
    
  
    particle.style.left = Math.random() * 100 + 'vw';
    particle.style.top = '100vh';
    
  
    const animation = particle.animate([
        { transform: 'translateY(0) scale(1)', opacity: 0.7 },
        { transform: `translateY(-${window.innerHeight + 100}px) scale(0.5)`, opacity: 0 }
    ], {
        duration: Math.random() * 3000 + 2000,
        easing: 'cubic-bezier(0.4, 0, 0.2, 1)'
    });
    
    animation.onfinish = () => particle.remove();
}


setInterval(createParticle, 500);