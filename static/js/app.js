

const mountEl = document.getElementById('app')
if (mountEl){

const app = Vue.createApp({
    delimiters: ["[[", "]]"],
    data() {
        return {
            question_number: 1,
            questions: [],
            loading: true,
            timeLeft: 3600,
            interval: null,
            selectedAnswer: null,
            storedAnswers:[],
            resetContinue: false,
            finish_test: false,
            progress:{}, // to store progress on local storage
            csrfToken: null,

        };
    },
    methods: {
        sendResults(){
          this.getCSRF()
          const mode = new URLSearchParams(window.location.search).get('mode');
          axios.post(`http://127.0.0.1:8000/api/save_test_results/?mode=${mode}`,this.storedAnswers,{
            headers:{
            'X-CSRFToken': this.csrfToken,
            'Content-Type': 'application/json'
            },
            withCredentials: true
          }).then(response => {
            console.log('Sent successfully')
          })
        },
        getCSRF(){
          this.csrfToken = document.cookie
          .split('; ')
          .find(row => row.startsWith('csrftoken='))
          ?.split('=')[1];
        },
        // stores the answer for use in the result page
        storeAnswer() {
            if (this.selectedAnswer !== null) {
              let index = this.storedAnswers.findIndex(
                item => item.id === this.question_number
              );
      
              if (index !== -1) {
                // ✅ Replace existing answer
                this.storedAnswers[index] = {
                  id: this.question_number,
                  answer: this.selectedAnswer,
                  correct_answer: this.questions[this.question_number -1].correct_answer
                };
              } else {
                // ✅ Add new answer
                this.storedAnswers.push({
                  id: this.question_number,
                  answer: this.selectedAnswer,
                  correct_answer: this.questions[this.question_number -1].correct_answer
                });
              }
              this.selectedAnswer = null; // Reset for next question
            } else {
              this.storedAnswers[this.question_number -1] = {
                id: this.question_number,
                answer: 'no answer provided',
                correct_answer: this.questions[this.question_number -1].correct_answer
              }
            }
          },
        countDown(){
            this.interval = setInterval(() => {
              if (this.timeLeft >0) {this.timeLeft--}
              else{
                clearInterval(this.interval)
                this.finishTest()
              }
            },1000)
            
        },
        nextQuestion() {
            // Only move to the next question if it exists
            if (this.question_number < this.questions.length) {
                this.storeAnswer();
                this.question_number++;
                this.saveState();
                this.restoreAnswer();
            } else {
                this.storeAnswer();
                this.finishTest()
                
            }
        },
        previousQuestion() {
            // Only move to the previous question if it's not negative
            if (this.question_number > 1) {
                this.question_number--;
                this.restoreAnswer();
            } else {}
        },
        // restore the previously selected or following answer and display it back to the screen
        restoreAnswer() {
            let found = this.storedAnswers.find(
                item => item.id === this.question_number
              );
              this.selectedAnswer = found ? found.answer : null; // Restore if found, else reset
        },
        finishTest() {
          this.saveState()
          this.finish_test = true
          this.clearState()
          this.sendResults()
          
          alert('The test is now finished')
        },
        // to store progress on local storage
        saveState(){
          this.progress = {
            time_left: this.timeLeft,
            question_number: this.question_number,
            answers: this.storedAnswers,
            questions: this.questions
            }
          localStorage.setItem('test_progress',JSON.stringify(this.progress))
        }, 
        // clear local storage once the test is complete
        clearState(){
          localStorage.removeItem('test_progress')
        },
        //check if the answer is correct
        checkAnswer(answer){
          if (answer.correct_answer){
            if (Object.values(answer.correct_answer).includes("N/A")){ return 'Your essay answer will be reviewed by an admin shortly'}
            else if (Object.values(answer.correct_answer).includes(answer.answer)){ return 'correct'} else {return 'incorrect'}
        } else {return 'Error while checking your answer'} 
      },
        resetTest(){
          localStorage.clear()
          this.resetContinue = false
          location.reload()
        },
        continueTest(){
          this.resetContinue = false
        },

        
    },
  async created() {
      try {
        //Loading local data if the test wasn't finished or page reloaded
          const saved = localStorage.getItem('test_progress')
            if (saved){
              this.resetContinue = true
              const data = JSON.parse(saved)
              this.question_number = data.question_number || 1
              this.storedAnswers = data.answers || []
              this.timeLeft = data.time_left || 3600
              this.questions = data.questions || []            
              }
            
          else {
            const response = await axios.get('http://127.0.0.1:8000/api/get_test_questions/');
            this.questions = response.data
            this.loading = false
          }
      } catch (error) {
          console.error ('Error fetching questions:',error);
      }
  },
  computed: {
      currentQuestion() {
        return this.questions[this.question_number -1] || { data : {}}; // Prevents undefined errors
      },
      formattedTime(){
          const minutes = Math.floor(this.timeLeft /60);
          const seconds = this.timeLeft % 60;
          return `${minutes.toString().padStart(2,"0")}:${seconds.toString().padStart(2,"0")}`
      },
      endOftest() {
        return this.question_number === this.questions.length
      },
    },
  mounted() {
        this.countDown()
      },
  beforeUnmount() {
        clearInterval(this.interval); // Clean up when component is destroyed
      },
});

try {app.mount('#app')
}
catch (error) {console.error ('Waiting for the test screen:',error);}
}
