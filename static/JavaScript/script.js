    // Gestion de l'affichage des fichiers sélectionnés
    document.querySelector('#extractForm input[type="file"]').addEventListener('change', function(e) {
      const fileName = e.target.files[0]?.name || 'Aucun fichier sélectionné';
      document.getElementById('videoFileSelected').textContent = `Fichier sélectionné: ${fileName}`;
      document.getElementById('videoFileSelected').style.display = 'block';
      document.getElementById('videoLabel').classList.add('pulse');
    });
    
    document.querySelector('#transcribeForm input[type="file"]').addEventListener('change', function(e) {
      const fileName = e.target.files[0]?.name || 'Aucun fichier sélectionné';
      document.getElementById('audioFileSelected').textContent = `Fichier sélectionné: ${fileName}`;
      document.getElementById('audioFileSelected').style.display = 'block';
      document.getElementById('audioLabel').classList.add('pulse');
    });

    // Animation au survol des labels
    document.getElementById('videoLabel').addEventListener('mouseenter', function() {
      this.classList.add('pulse');
    });
    
    document.getElementById('videoLabel').addEventListener('mouseleave', function() {
      if (!document.querySelector('#extractForm input[type="file"]').files.length) {
        this.classList.remove('pulse');
      }
    });
    
    document.getElementById('audioLabel').addEventListener('mouseenter', function() {
      this.classList.add('pulse');
    });
    
    document.getElementById('audioLabel').addEventListener('mouseleave', function() {
      if (!document.querySelector('#transcribeForm input[type="file"]').files.length) {
        this.classList.remove('pulse');
      }
    });

    // Gestion des formulaires
    async function handleForm(event, formId, loaderId, progressId, progressTextId, statusId) {
      event.preventDefault();
      const form = event.target;
      const loader = document.getElementById(loaderId);
      const progressBar = document.getElementById(progressId);
      const progressText = document.getElementById(progressTextId);
      const statusMessage = document.getElementById(statusId);
      const submitBtn = form.querySelector('button[type="submit"]');
      
      // Désactiver le bouton pendant le traitement
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Traitement...';
      
      // Afficher le loader
      loader.style.display = 'block';
      statusMessage.style.display = 'block';
      statusMessage.textContent = 'Préparation du traitement...';
      
      // Animation de progression simulée
      let progress = 0;
      const progressInterval = setInterval(() => {
        if (progress < 90) {
          progress += Math.random() * 10;
          progress = Math.min(progress, 90);
          progressBar.style.width = `${progress}%`;
          progressText.textContent = `${Math.round(progress)}% complété`;
          
          // Messages de statut dynamiques
          if (progress < 30) {
            statusMessage.textContent = 'Analyse du fichier...';
          } else if (progress < 60) {
            statusMessage.textContent = 'Extraction des données...';
          } else {
            statusMessage.textContent = 'Finalisation du traitement...';
          }
        }
      }, 500);
      
      try {
        const formData = new FormData(form);
        const response = await fetch(form.action, {
          method: 'POST',
          body: formId === 'summaryForm' ? JSON.stringify({ text: document.getElementById('summaryText').value }) : formData,
          headers: formId === 'summaryForm' ? { 'Content-Type': 'application/json' } : {}
        });
        
        const data = await response.json();
        
        // Compléter la barre de progression
        clearInterval(progressInterval);
        progress = 100;
        progressBar.style.width = `${progress}%`;
        progressText.textContent = `${progress}% complété`;
        statusMessage.textContent = 'Traitement terminé avec succès!';
        statusMessage.style.color = 'var(--success)';
        
        // Afficher les résultats
        displayResult(data);
        
        // Réactiver le bouton après un délai
        setTimeout(() => {
          submitBtn.disabled = false;
          submitBtn.innerHTML = formId === 'extractForm' ? '<i class="fas fa-cogs"></i> Extraire l\'audio' : 
                             formId === 'transcribeForm' ? '<i class="fas fa-keyboard"></i> Transcrire' : 
                             '<i class="fas fa-compress-alt"></i> Résumer';
        }, 1000);
        
      } catch (error) {
        clearInterval(progressInterval);
        statusMessage.textContent = 'Erreur lors du traitement: ' + error.message;
        statusMessage.style.color = 'var(--warning)';
        progressBar.style.backgroundColor = 'var(--warning)';
        
        // Réactiver le bouton
        submitBtn.disabled = false;
        submitBtn.innerHTML = formId === 'extractForm' ? '<i class="fas fa-cogs"></i> Extraire l\'audio' : 
                           formId === 'transcribeForm' ? '<i class="fas fa-keyboard"></i> Transcrire' : 
                           '<i class="fas fa-compress-alt"></i> Résumer';
      }
    }
    
    // Attacher les gestionnaires d'événements
    document.getElementById('extractForm').addEventListener('submit', (e) => {
      handleForm(e, 'extractForm', 'extractLoader', 'extractProgress', 'extractProgressText', 'extractStatus');
    });
    
    document.getElementById('transcribeForm').addEventListener('submit', (e) => {
      handleForm(e, 'transcribeForm', 'transcribeLoader', 'transcribeProgress', 'transcribeProgressText', 'transcribeStatus');
    });
    
    document.getElementById('summaryForm').addEventListener('submit', (e) => {
      handleForm(e, 'summaryForm', 'summaryLoader', 'summaryProgress', 'summaryProgressText', 'summaryStatus');
    });
    
    // Fonction d'affichage des résultats
    function displayResult(data) {
      const output = document.getElementById('resultOutput');
      let resultHTML = '';
      
      if (data.audio_path) {
        resultHTML += `<div class="result-section">
          <h3><i class="fas fa-check-circle" style="color: var(--success)"></i> Audio extrait avec succès</h3>
          <p>${data.audio_path}</p>
        </div>`;
      }
      
      if (data.transcription) {
        resultHTML += `<div class="result-section">
          <h3><i class="fas fa-check-circle" style="color: var(--success)"></i> Transcription générée</h3>
          <p>${data.transcription}</p>
        </div>`;
      }
      
      if (data.summary) {
        resultHTML += `<div class="result-section">
          <h3><i class="fas fa-check-circle" style="color: var(--success)"></i> Résumé généré</h3>
          <p>${data.summary}</p>
        </div>`;
      }
      
      if (!resultHTML) {
        resultHTML = `<div class="result-section">
          <h3><i class="fas fa-exclamation-triangle" style="color: var(--warning)"></i> Aucune donnée à afficher</h3>
          <p>Le traitement n'a pas retourné de résultats.</p>
        </div>`;
      }
      
      output.innerHTML = resultHTML;
      
      // Ajouter une animation pour le résultat
      output.style.animation = 'none';
      void output.offsetWidth; // Déclenche un reflow
      output.style.animation = 'fadeIn 0.5s ease-out';
    }
    
    // Ajouter une animation CSS dynamiquement
    const style = document.createElement('style');
    style.textContent = `
      @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
      }
      
      .result-section {
        margin-bottom: 1.5rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid var(--gray-light);
      }
      
      .result-section:last-child {
        margin-bottom: 0;
        padding-bottom: 0;
        border-bottom: none;
      }
      
      .result-section h3 {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
        color: var(--dark);
      }
      
      .result-section p {
        background-color: white;
        padding: 1rem;
        border-radius: 6px;
        border-left: 3px solid var(--accent);
      }
    `;
    document.head.appendChild(style);