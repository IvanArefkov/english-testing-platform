
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
            finish_test: false,
            progress:{}, // to store progress on local storage
        };
    },
    async created() {
        try {
            const response = await axios.get('http://127.0.0.1:8000/tests/get_test_questions/');
            console.log(response.data)
            this.questions = response.data;
            this.loading = false;
            //Loading local data if the test wasn't finished or page reloaded
            const saved = localStorage.getItem('test_progress')
            if (saved){
              const data = JSON.parse(saved)
              this.question_number = data.question_number || 1
              this.storedAnswers = data.answers || []
              this.timeLeft = data.time_left || 3600
            }
            console.log(this.questions.length);
        } catch (error) {
            console.error ('Error fetching questions:',error);
        }
    },
    computed: {
        currentQuestion() {
          return this.questions[this.question_number -1] || { fields : {}}; // Prevents undefined errors
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
    methods: {
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
                  correct_answer: this.questions[this.question_number].fields.correct_answer
                };
              } else {
                // ✅ Add new answer
                this.storedAnswers.push({
                  id: this.question_number,
                  answer: this.selectedAnswer,
                  correct_answer: this.questions[this.question_number -1].fields.correct_answer
                });
              }
      
              console.log("Stored Answers:", this.storedAnswers);
              this.selectedAnswer = null; // Reset for next question
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
                console.log(this.question_number,this.questions.length);
                this.restoreAnswer();
            } else {
                console.log (this.question_number, this.questions.length)
                this.storeAnswer();
                this.finishTest()
                console.log("You are on the last question.");
            }
        },
        previousQuestion() {
            // Only move to the previous question if it's not negative
            if (this.question_number > 1) {
                this.question_number--;
                this.restoreAnswer();

            } else {
                console.log("You are on the first question.");
            }
        },
        // restore the previously selected answer and display it back to the screen
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
          console.log(this.storedAnswers)
          alert('The test is now finished')
        },
        // to store progress on local storage
        saveState(){
          this.progress = {
            time_left: this.timeLeft,
            question_number: this.question_number,
            answers: this.storedAnswers,
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
          if (Object.values(answer.correct_answer).includes(answer.answer)){ return 'correct'} else {return 'incorrect'}
        } else {return 'N/A'} 
      },
        
    },
    mounted() {
        this.countDown()
      },
    beforeUnmount() {
        clearInterval(this.interval); // Clean up when component is destroyed
      },
});

app.mount('#app');
