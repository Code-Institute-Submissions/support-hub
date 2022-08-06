# Testing

## Automated Tests

Due to the time constraints of this project, partial automated testing was implemented as part of the release phase.

## Manual Tests

### Methodology

Manual testing occurred regularly throughout local development, making use of statements that would print information to the console and use of the Django debug pages.

Each function of the website had specific testing requirements which were documented as test cases. The aim of documenting these test cases was that they could be run before pull requests were committed to ensure no breaking changes were introduced. Tests were documented as the site evolved so new tests for new functionality could be easily added.

### Test Cases

&nbsp;

#### Registration Page

| Testing | Test # | Steps | Expected Outcome | Results |
| - | - | - | - | - |
| Form Validation | 1 | Try to submit empty form | Form validation will prompt for user action | PASS |
| Form Validation | 2 | Try to submit invalid email address  | Form validation will prompt for user action | PASS |
| Form Validation | 3 | Try to submit username that is already taken | Form validation will prompt for user action | PASS |
| Form Validation | 4 | Try to submit non-complex, not matching passwords | Form validation will prompt for user action | PASS |
| Form Validation | 5 | Remove the required attribute using browser console tools and submit with no first or last name but other valid fields | Form validation will prompt for user action | PASS |
| Registration success | 6 | Enter unique, valid information for all fields | User is notified with a success message and redirected to the email verification page. Verification email is send to email address entered in registration form. Account can be seen in the Django admin panel | PASS |

&nbsp;

#### Create and Edit Tickets

Tests for the creation and editing of tickets were completed using an account with the role of Customer followed by an account with the role of Technician. The following tests are applicable for ticket creation and editing so are repeated for each activity.

| Testing | Test # | Steps | Expected Outcome | Results |
| - | - | - | - | - |
| Text Field Validation | 1 | Try to submit empty form |  | PASS |
| Text Field Validation | 2 | Enter a description with leading white-space and submit the form | Form validation will prompt for user action | PASS |
| Text Field Validation | 3 | Enter a description and title with fewer characters than the required amount (10 for title and 20 fro description) and submit the form | Form validation will prompt for user action | PASS |
| Image Field Validation | 4 | Try to upload a GIF | Form validation will notify the user the image format is not permitted and remind them of the accepted formats | PASS |
| Image Field Validation | 5 | Try to upload a PDF | Form validation will notify the user the image format is not permitted and remind them of the accepted formats | PASS |
| Image Field Validation | 6 | Try to upload a JPEG larger than 3MB | Form validation will notify the user the image is too large (bytes) and remind them of the maximum accepted file size | PASS |
| Image Field Validation | 7 | Try to upload a Text file with the file extension changed to png | Form validation will notify the user the image format is not valid or corrupted | PASS |
| Image Field Validation | 8 | Try to upload a CSV file with the file extension changed to png | Form validation will notify the user the image format is not valid or corrupted  | PASS |
| Image Field Validation | 9 | Enter valid information for all fields | Ticket created, user redirected to the newly created tickets detail view and notified via message. Ticket matches all information as entered in the form (author, status, etc.) | PASS |

&nbsp;

#### Ticket Deletion

| Testing | Test # | Steps | Expected Outcome | Results |
| - | - | - | - | - |
| Delete button visible to Elevated users | 1 | Log in as an elevated user, navigate to a ticket detail view and ensure deleted button is visible | Delete button visible | PASS |
| Delete button prompts user to confirm ticket deletion | 2 | Use the delete button and ensure the deletion confirmation model is displayed containing confirmation and cancel buttons | Model opens displaying the correct options | PASS |
| Ticket can be deleted | 3 | Click the deletion confirmation button in the model | Ticket is deleted, ticket images (if any) are removed from Cloudinary. User is redirected to the ticket list view and notified with a message | PASS |
| Ticket cannot be deleted by Customers if button made visible | 4 | Make button visible in the ticket detail template and login as customer before trying to delete a ticket | User is notified they do not have permissions to delete a ticket with a message | PASS |
| Delete button not visible to customers | 5 | Log in as customer, navigate to a ticket detail view and ensure deleted button is not visible | Only edit buttons is visible in the ticket detail actions card | PASS |

&nbsp;

#### Navigation and Ticket View

| Testing | Test # | Steps | Expected Outcome | Results |
| - | - | - | - | - |
| Customer can view ticket where they are the author | 1 | Navigate to a ticket detail URL where the logged on customer is the author | Ticket detail is visible | PASS |
| Customer cannot view the tickets of other users | 2 | Navigate to a ticket detail URL where the logged on customer is not the author | Redirected to a 403 page | PASS |
| Elevated users can view ticket where they are the author | 3 | Navigate to a ticket detail URL where the logged on technician is the author | Ticket detail is visible | PASS |
| Customer can view their own profile | 4 | Navigate to a logged on customer profile page | Profile is visible | PASS |
| Customer cannot view the profiles of other users | 5 | Navigate to the profile of another valid user using a manually input URL | Redirected to a 403 page | PASS |
| Technician can view their own profile | 6 | Navigate to a logged on customer profile page | Profile is visible | PASS |
| Technician cannot view the profiles of other users | 7 | Navigate to the profile of another valid user using a manually input URL | Redirected to a 403 page | PASS |
| Using a string as a ticket slug | 8 | Enter a URL using a string as a ticket slug (.../tickets/invalid) | Redirected to home page and user informed with error message | PASS |
| Using a string as a ticket slug | 9 | Enter a URL using a string as a ticket slug (.../tickets/invalid/edit) | Redirected to home page and user informed with error message | PASS |
| Using a string as a ticket slug | 10 | Enter a URL using a string as a ticket slug (.../accounts/profile/invalid) | Redirected to home page and user informed with error message | PASS |
| Using a string as a ticket slug | 11 | Enter a URL using a string as a ticket slug (.../accounts/profile/invalid/edit) | Redirected to home page and user informed with error message | PASS |

&nbsp;

#### User Search

| Testing | Test # | Steps | Expected Outcome | Results |
| - | - | - | - | - |
| Only administrator role can view User Search page | 1 | Login as customer and check if the navigation link to the user search is visible and try to navigate to the url manually | Link to user search not visible and will be redirected to 403 page | PASS |
| Only administrator role can view User Search page | 2 | Login as technician check if the navigation link to the user search is visible and try to navigate to the url manually | Link to user search not visible and will be redirected to 403 page | PASS |
| Only administrator role can view User Search page | 3 | Login as administrator,  check if the navigation link to the user search is visible and try to navigate to the url manually | Link to user search is visible and user search page loads | PASS |
| User search returns results which can be viewed | 4 | Logged in as Administrator, queries return accurate results which can be visited | User search results are accurate and a profile of another user can be viewed | PASS |
| Profiles can be edited and only Role and Team can be changed | 5 | Logged in as Administrator, visiting the user profile of another user and selecting to edit.. the role and team can be successfully saved | User Role and Team can be changed. | PASS |

&nbsp;

#### Profile View and Edit (other than administrator)

| Testing | Test # | Steps | Expected Outcome | Results |
| - | - | - | - | - |
| Form Validation | 1 | Change first and last name and try to submit | From validation will prompt for user action | PASS |
| Form Validation | 2 | Enter username that is already taken | From validation will prompt for user action | PASS |
| Profile edit success | 3 |  Enter unique |  valid information for all fields  | User is notified with a message and redirected profile detail page | PASS |

&nbsp;

## Code Validation

### HTML

The [W3C Markup Validator](https://validator.w3.org/nu/) and [W3C CSS Validator](https://jigsaw.w3.org/css-validator/) Services were used to validate the project's HTML and CSS files to ensure there were no syntax errors or warnings.

Tests passed with the exception of pages that made use of the *django-summernote* widget. The majority of these errors were fixed (as discussed in the [Changes as a result of testing](#changes-as-a-result-of-testing) and the [bugs](README.md#bugs) sections), but one error caused by *django-summernote* widget has been ignored.

![HTML validation error 3](docs/validation/html/w3c-html-validation-service-error-3.png)

The error is caused by *django-summernote* setting the hidden attribute on a textarea element within it's python code [Link to django-summernote source - widgets.py](https://github.com/summernote/django-summernote/blob/main/django_summernote/widgets.py#L49). This error has been ignored and this is clearly visible in the screenshots of tests.

Please click the page name to view a screenshot of the validation check.

| Page | Result |
| - | - |
| [Home Page - Not Authenticated](docs/validation/html/w3c-html-validation-service-homepage-notauthenticated.png) | PASS |
| [Home Page - Authenticated](docs/validation/html/w3c-html-validation-service-homepage-authenticated-with-toast.png) | PASS |
| [Ticket List Page](docs/validation/html/w3c-html-validation-service-tickets-list.png) | PASS |
| [Ticket Detail Page](docs/validation/html/w3c-html-validation-service-tickets-detail.png) | PASS* |
| [Ticket Create Page - Customer](docs/validation/html/w3c-html-validation-service-tickets-create-customer.png) | PASS* |
| [Ticket Create Page - Customer](docs/validation/html/w3c-html-validation-service-tickets-create-technician.png) | PASS* |
| [Ticket Edit Page - Customer](docs/validation/html/w3c-html-validation-service-profile-edit.png) | PASS* |
| [Ticket Edit Page - Elevated](docs/validation/html/w3c-html-validation-service-profile-edit-administrator.png) | PASS* |
| [Profile View Page](docs/validation/html/w3c-html-validation-service-profile.png) | PASS |
| [Profile Edit Page - Customer](docs/validation/html/w3c-html-validation-service-profile-edit.png) | PASS |
| [Profile Edit Page - Administrator](docs/validation/html/w3c-html-validation-service-profile-edit-administrator.png) | PASS |
| [Profile Search Page](docs/validation/html/w3c-html-validation-service-profile-search-administrator.png) | PASS |

\* Passed with known error ignored, caused by *django-summernote*.

### CSS

No validation errors reported.

- [Results for CSS](docs/validation/css/w3c-css-validation-service-results.png)

#### Changes as a result of testing

Link alt text was changed to use the title attribute based on the following error returned from the validation tool:

![HTML Validation Error 1](docs/validation/html/w3c-html-validation-service-error-1.png)

The SummernoteWidget makes use of an iFrame which was being loaded with attributes that caused HTML validation errors.

[Link to HTML Validation Error 2](docs/validation/html/w3c-html-validation-service-error-2.png)

To correct this I made a copy of the 'widget_iframe' template to my root templates directory so it is selected first. I then edited the template to remove the attributes causing validation errors, replacing the width with CSS.

### Python

No validation error reported when using the [PEP8 Online Check Tool](http://pep8online.com/)

| App/Parent folder | File | Result |
| - | - | - |
| accounts | [admin.py](docs/validation/python/pep8online-accounts-admin.png) | PASS |
| accounts | [forms.py](docs/validation/python/pep8online-accounts-forms.png) | PASS |
| accounts | [models.py](docs/validation/python/pep8online-accounts-models.png) | PASS |
| accounts | [urls.py](docs/validation/python/pep8online-accounts-urls.png) | PASS |
| accounts | [views.py](docs/validation/python/pep8online-accounts-views.png) | PASS |
| accounts/tests | [test_urls.py](docs/validation/python/pep8online-accounts-test-urls.png) | PASS |
| common | [utils.py](docs/validation/python/pep8online-common-utils.png) | PASS |
| tickets | [admin.py](docs/validation/python/pep8online-tickets-admin.png) | PASS |
| tickets | [apps.py](docs/validation/python/pep8online-tickets-apps.png) | PASS |
| tickets | [filters.py](docs/validation/python/pep8online-tickets-filters.png) | PASS |
| tickets | [forms.py](docs/validation/python/pep8online-tickets-forms.png) | PASS |
| tickets | [models.py](docs/validation/python/pep8online-tickets-models.png) | PASS |
| tickets | [signals.py](docs/validation/python/pep8online-tickets-signals.png) | PASS |
| tickets | [urls.py](docs/validation/python/pep8online-tickets-urls.png) | PASS |
| tickets | [utils.py](docs/validation/python/pep8online-tickets-utils.png) | PASS |
| tickets | [validators.py](docs/validation/python/pep8online-tickets-validators.png) | PASS |
| tickets | [views.py](docs/validation/python/pep8online-tickets-views.png) | PASS |
| tickets/tests | [test_forms.py](docs/validation/python/pep8online-tickets-test-forms.png) | PASS |
| tickets/tests | [test_models.py](docs/validation/python/pep8online-tickets-test-models.png) | PASS |
| tickets/tests | [test_urls.py](docs/validation/python/pep8online-tickets-test-urls.png) | PASS |
| tickets/tests | [test_views.py](docs/validation/python/pep8online-tickets-test-views.png) | PASS |

### JavaScript

No validation errors reported testing with [JSHint](https://jshint.com).

![Results for JavaScript](docs/validation/javascript/jshint-results.png)

## WAVE - Web Accessibility Evaluation Tool

All pages were tested using the [WAVE Firefox extension](https://wave.webaim.org/extension/). No errors were returned for any pages and the report for the homepage can be viewed below:

![Results for JavaScript](docs/validation/wave/wave-report-supporthub-homepage.png)

## Lighthouse Scores

Most pages of the site when tested with a desktop or mobile device view performed very well, with pages scoring above 90% for performance and accessibility, and 100% for Best Practices. 2 pages under mobile device testing dropped to 87% performance (with this number varying slightly under repeated testing).

Original ticket creation page score - Mobile

![Original ticket creation page score](docs/validation/lighthouse/lighthouse-report-ticket-create-mobile.png)

Original ticket list page score - Mobile

![Original ticket list page score](docs/validation/lighthouse/lighthouse-report-ticket-list-mobile.png)

After investigation this issue was caused due to leaving script tags in the head element which was blocking the first paint of the page (an oversight left in place from early development work). Also the summernote iframe did not have a title, as I had altered the template to correct other problems (detailed in the [Bugs](README.md#bugs) section), I simply added a title to the iframe element manually.

Once the script tags were moved to the bottom on the body element and the iframe title added, site performance improved on all pages with only the ticket detail page scoring less than 90%. This was due to loading CSS files from Bootstrap and Cloudinary and requires future work to fully investigate and resolve.

Ticket creation page score (updated) - Mobile

![Ticket creation page mobile score](docs/validation/lighthouse/lighthouse-report-ticket-create-mobile-postfix.png)

Ticket list page score (updated) - Mobile

![Ticket list page mobile score](docs/validation/lighthouse/lighthouse-report-ticket-list-mobile-postfix.png)

Home page score - Desktop

![Home page desktop score](docs/validation/lighthouse/lighthouse-report-homepage-desktop.png)

Home page score - Mobile

![Home page mobile score](docs/validation/lighthouse/lighthouse-report-homepage-mobile.png)

Please see the [docs/validation/lighthouse/pdf](docs/validation/lighthouse/pdf) folder for summary lighthouse reports.

## Devices used for manual testing

Site was tested using the following desktop and mobile browsers:

- Chrome (v.103), Firefox (v.103), Firefox Developer Edition (v.104), GNOME Web (v.41.3, using WebKitGTK 2.34.4), Safari (iOS 15 on iPhone 7 and iPad 6th Gen).

Return to [README.md](README.md#support-hub)
