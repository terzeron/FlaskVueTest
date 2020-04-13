<template>
    <b-container>
        <b-row>
            <b-col col sm="10">
                <h1>Books</h1>
                <hr><br><br>
                <alert :message="message" v-if="showMessage"></alert>
                <button type="button" class="btn btn-success btn-sm" v-b-modal.book-modal>Add Book</button>
                <br><br>
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th scope="col">Title</th>
                            <th scope="col">Author</th>
                            <th scope="col">Read?</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(book, index) in books" :key="index">
                            <td>{{ book.title }}</td>
                            <td>{{ book.author }}</td>
                            <td>
                                <span v-if="book.read">Yes</span>
                                <span v-else>No</span>
                            </td>
                            <td>
                                <div class="btn-group" role="group">
                                    <button type="button" class="btn btn-warning btn-sm" v-b-modal.book-update-modal @click="editBook(book)">Update</button>
                                    <button type="button" class="btn btn-danger btn-sm" @click="onDeleteBook(book)">Delete</button>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </b-col>
        </b-row>
        
        <b-modal ref="addBookModal"
                 id="book-modal"
                 title="Add a new book"
                 hide-footer>
            <b-form @submit="onSubmit" @reset="onReset" class="w-100">
                <b-form-group id="form-title-group"
                              label="Title:"
                              label-for="form-title-input">
                    <b-form-input id="form-title-input"
                                  type="text"
                                  v-model="addBookForm.title"
                                  required
                                  placeholder="Enter title">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-author-group"
                              label="Author:"
                              label-for="form-author-input">
                    <b-form-input id="form-author-input"
                                  type="text"
                                  v-model="addBookForm.author"
                                  required
                                  placeholder="Enter author">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-read-group">
                    <b-form-checkbox v-model="addBookForm.read" id="form-checks">Read?</b-form-checkbox>
                </b-form-group>
                <b-button type="submit" variant="primary">Submit</b-button>
                <b-button type="reset" variant="danger">Reset</b-button>
            </b-form>
        </b-modal>

        <b-modal ref="editBookModal"
                 id="book-update-modal"
                 title="Update"
                 hide-footer>
            <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
                <b-form-group id="form-title-edit-group"
                              label="Title:"
                              label-for="form-title-edit-input">
                    <b-form-input id="form-title-edit-input"
                                  type="text"
                                  v-model="editForm.title"
                                  required
                                  placeholder="Enter title">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-author-edit-group"
                              label="Author:"
                              label-for="form-author-edit-input">
                    <b-form-input id="form-author-edit-input"
                                  type="text"
                                  v-model="editForm.author"
                                  required
                                  placeholder="Enter author">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-read-edit-group">
                    <b-form-checkbox v-model="editForm.read" id="form-checks">Read?</b-form-checkbox>
                </b-form-group>
                <b-button-group>
                    <b-button type="submit" variant="primary">Update</b-button>
                    <b-button type="reset" variant="danger">Cancel</b-button>
                </b-button-group>
            </b-form>
        </b-modal>
    </b-container>
</template>

<script>
 import axios from 'axios';
 import Alert from './Alert';
 
 export default {
     name: 'Books',
     data() {
         return {
             books: [],
             addBookForm: {
                 title: '',
                 author: '',
                 read: false,
             },
             editForm: {
                 id: '',
                 title: '',
                 author: '',
                 read: false,
             },
             message: '',
             showMessage: false,
         };
     },
     components: {
         alert: Alert,
     },
     methods: {
         getBooks() {
             const path = 'https://api.terzeron.com/book/books';
             axios.get(path)
                  .then((res) => {
                      this.books = res.data.books;
                  })
                  .catch((error) => {
                      console.error(error);
                  });
         },
         addBook(payload) {
             const path = 'https://api.terzeron.com/book/books';
             axios.post(path, payload)
                  .then(() => {
                      this.getBooks();
                      this.message = 'Book added!';
                      this.showMessage = true;
                  })
                  .catch((error) => {
                      console.error(error);
                      this.getBooks();
                  })
         },
         updateBook(payload, bookID) {
             const path = `https://api.terzeron.com/book/books/${bookID}`;
             axios.put(path, payload)
                  .then(() => {
                      this.getBooks();
                      this.message = 'Book updated!';
                      this.showMesage = true;
                  })
                  .catch((error) => {
                      console.error(error);
                      this.getBooks();
                  });
         },
         editBook(book) {
             this.editForm = book;
         },
         removeBook(bookID) {
             const path = `https://api.terzeron.com/book/books/${bookID}`;
             axios.delete(path)
                  .then(() => {
                      this.getBooks();
                      this.message = 'Book removed!';
                      this.showMessage = true;
                  })
                  .catch((error) => {
                      console.error(error);
                      this.getBooks();
                  });
         },
         onDeleteBook(book) {
             this.removeBook(book.id);
         },
         initForm() {
             this.addBookForm.title = '';
             this.addBookForm.author = '';
             this.addBookForm.read = false;
             this.editForm.id = '';
             this.editForm.title = '';
             this.editForm.author = '';
             this.editForm.read = false;
         },
         onSubmit(evt) {
             evt.preventDefault();
             this.$refs.addBookModal.hide();
             const payload = {
                 title: this.addBookForm.title,
                 author: this.addBookForm.author,
                 read: this.addBookForm.read,
             };
             this.addBook(payload);
             this.initForm();
         },
         onSubmitUpdate(evt) {
             evt.preventDefault();
             this.$refs.editBookModal.hide();
             const payload = {
                 title: this.editForm.title,
                 author: this.editForm.author,
                 read: this.editForm.read,
             };
             this.updateBook(payload, this.editForm.id);
         },
         onReset(evt) {
             evt.preventDefault();
             this.$refs.addBookModal.hide();
             this.initForm();
         },
         onResetUpdate(evt) {
             evt.preventDefault();
             this.$refs.editBookModal.hide();
             this.initForm();
             this.getBooks();
         },
     },
     created() {
         this.getBooks();
     },
 };
</script>
