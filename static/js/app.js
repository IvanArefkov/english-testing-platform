
const app = Vue.createApp({
    delimiters: ["[[", "]]"],
    data() {
        return {
            question_number: 1,
            questions: [],
            loading: true,
            timeLeft: 3600,
            selectedAnswer: null,
            storedAnswers:[],
            finish_test: false,
        };
    },
    async created() {
        try {
            const response = await axios.get('http://127.0.0.1:8000/tests/get_test_questions/');
            console.log(response.data)
            this.questions = response.data;
            this.loading = false;
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
        }
      },
    methods: {
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
            if(this.timeLeft<1){
                alert('The time is out')
                this.timeLeft=0
            }else{this.timeLeft--}
            
        },
        nextQuestion() {
            // Only move to the next question if it exists
            if (this.question_number < this.questions.length) {
                this.storeAnswer();
                this.question_number++;
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
        restoreAnswer() {
            let found = this.storedAnswers.find(
                item => item.id === this.question_number
              );
              this.selectedAnswer = found ? found.answer : null; // Restore if found, else reset
            },
        finishTest() {
          this.finish_test = true
          console.log(this.storedAnswers)
        }
        
    },
    mounted() {
        this.interval = setInterval(this.countDown, 1000); // Run every second
      },
      beforeUnmount() {
        clearInterval(this.interval); // Clean up when component is destroyed
      },
});

app.mount('#app');
