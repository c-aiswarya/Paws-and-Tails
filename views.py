from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .import models
from .models import Donation_amount, user_reg,Pet, trainer_reg,Adopt,Pay,Vaccinations,Muncipality
from .models import Timetable
import razorpay
import smtplib
from datetime import datetime
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

# Create your views here.
def index(request):
    return render(request,'index.html')

def logout(request):
    request.session.flush()
    return redirect('index')

def user_home(request):
    return render(request,'user_home.html')

#userreg

def userregistration(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phno = request.POST.get('phno')
        place = request.POST.get('place')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        image = request.FILES.get('image')
        idproof = request.POST.get('idproof')

        if password != confirm_password:
            msg = "Passwords do not match"
            return render(request, 'userregistration.html', {'msg': msg})

        if user_reg.objects.filter(email=email).exists():
            alert_message = "<script>alert('EMAIL ALREADY EXIST');window.location.href='/userregistration/';</script>"
            return HttpResponse(alert_message)
    
        user_reg(name=name, email=email, phno=phno, place=place, password=password, image=image, confirm_password=confirm_password , idproof=idproof).save()
        
        return redirect('userlogin')
    else:
        return render(request, 'userregistration.html')

      
#userlog

def userlogin(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        cr=user_reg.objects.filter(email=email,password=password)
        if cr:
            userd=user_reg.objects.get(email=email,password=password)
            id=userd.id
            email=userd.email
            password=userd.password
            request.session['id']=id
            request.session['email']=email
            request.session['password']=password
            return redirect('user_home')
        else:
            msg = 'invalid password or email'
            return render(request,'userlogin.html', {'msg':msg})
    return render(request,'userlogin.html') 

# userprofile
def profile(request):
    email = request.session.get('email')
    if not email:
        return render(request, 'userlogin.html', {'error': 'User not logged in'})
    admin = get_object_or_404(user_reg, email=email)
    user_info = {
        'adminname': admin.name,       
        'phno': admin.phno,
        'email': admin.email,
        'password': admin.password,
        'confirm_password': admin.confirm_password,
        'image': admin.image
    }
    return render(request, 'user_profile.html', user_info)
#userprofileupdate
def update_profile(request):
    email=request.session['email']
    cr =user_reg.objects.get(email=email)
    if cr:
        user_info = {
            'adminname':cr.name,
            'phno':cr.phno,
            'email':cr.email,
            'password':cr.password,
            'confirm_password':cr.confirm_password,
            'image':cr.image
        }
        return render(request,'update_profile.html',user_info)
    else:
        return render(request,'update_profile.html')

def proupdate(request):
    email = request.session.get('email')
    if not email:
        return redirect('adminlogin') 
    if request.method == "POST":
        user = user_reg.objects.get(email=email)
        adminname = request.POST.get('adminname')
        phno = request.POST.get('phno')
        confirm_password = request.POST.get('confirm_password')
        image = request.FILES.get('image')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user.adminname = adminname
        user.phno = phno
        user.confirm_password = confirm_password
        user.phno = phno
        user.email = email
        user.password = password
        
        if image:
            user.image = image
        
        user.save()
        
        user_info = {
            'adminname': user.adminname,
            'phno': user.phno,
            'confirm_password': user.confirm_password,
            'phno': user.phno,
            'email': user.email,
            'password': user.password,
            'image': user.image,
        }
        
        return render(request, 'user_profile.html', user_info)
    else:
        return render(request, 'update_profile.html')
#petlist
def pet_list(request):
    pets = Pet.objects.all()
    return render(request, 'pet_list.html', {'pets': pets})


#petdetails
def pet_detail(request, pk):
    pet = get_object_or_404(Pet.objects.select_related('muncipality'), pk=pk)  # Use select_related to include municipality details
    return render(request, 'pet_detail.html', {'pet': pet})

#adoption
def adopt(request, id):
    email = request.session.get('email')

    ar=Pet.objects.get(id=id) 
    dogname= ar.dogname
    breed=ar.breed
    age=ar.age
    muncipality_name = ar.muncipality.muncipality_name

    return render(request,"adopt.html",{'dogname':dogname,'breed':breed,'age':age,'email':email,'muncipality_name':muncipality_name})
from django.shortcuts import render, get_object_or_404
from .models import Pet, Adopt, user_reg, Muncipality

from django.shortcuts import get_object_or_404, render
from .models import Adopt, Muncipality, Pet, user_reg

def ado_pt(request):
    if request.method == 'POST':
        dogname = request.POST.get('dogname')
        breed = request.POST.get('breed')
        age = request.POST.get('age')
        email = request.session.get('email')  # Getting the email from the session
        muncipality_name = request.POST.get('muncipality_name')

        # Ensure email exists in the session before proceeding
        if email:
            try:
                # Retrieve the user details using the email from the session
                cr = user_reg.objects.get(email=email)
                name = cr.name
                place = cr.place
                idproof = cr.idproof

                # Fetch the pet based on the dogname, breed, and age
                pet = get_object_or_404(Pet, dogname=dogname, breed=breed, age=age)

                # Fetch the municipality object using muncipality_name (ensure it exists)
                muncipality = get_object_or_404(Muncipality, muncipality_name=muncipality_name)

                # Save adoption details to the database
                if dogname and breed and age and muncipality:
                    adoption = Adopt.objects.create(
                        dogname=dogname,  # The dog's name
                        breed=breed,      # The breed of the dog
                        age=age,          # The dog's age
                        muncipality_name=muncipality,  # Municipality linked to the adoption
                        idproof=idproof,  # ID proof of the adopter
                        name=name,         # Name of the adopter
                        email=email,       # Email of the adopter
                        place=place        # Place of the adopter (optional)
                    )

                    # Delete the pet after adoption (optional, based on your requirement)
                    

                    # Return a success message after successful adoption
                    return render(request, 'user_home.html', {'message': 'Adoption successful!'})

                else:
                    # Return an error message if any field is missing
                    return render(request, 'adopt.html', {'error': 'All fields are required.'})
            except user_reg.DoesNotExist:
                # Handle case where user_reg with the provided email doesn't exist
                return render(request, 'adopt.html', {'error': 'User not found.'})

    # If the request is not POST, simply render the adopt page
    return render(request, 'adopt.html')



def user_adopt(request):
    email = request.session.get('email')
    if email:
        adoption = Adopt.objects.filter(email=email)
            
    return render(request, 'user_adopt.html', {'a': adoption})


#searchforpets
def searchdog(request):
    if request.method =='POST':
        l=request.POST.get('breed')
        data=Pet.objects.filter(breed=l)
        return render(request,'searchdog.html',{'datas': data})
    return render(request,'searchdog.html')





def searchdogmuncipality(request):
    if request.method == 'POST':
        muncipality_name = request.POST.get('muncipality_name') 
        
        # Find the first matching Muncipality instance by name
        muncipality = Muncipality.objects.filter(muncipality_name=muncipality_name).first()
        
        # If a matching muncipality is found, filter Pet instances by it
        data = Pet.objects.filter(muncipality=muncipality) if muncipality else []
        
        return render(request, 'searchdogmuncipality.html', {'datas': data})
    
    return render(request, 'searchdogmuncipality.html')


from django.shortcuts import render, redirect
from .models import Pet, Dog_feddback

def dog_feedback(request, pet_id):
    # Retrieve dog details from the Pet model using the provided ID
    pet = Adopt.objects.get(id=pet_id)
    
    # Get the email from the session
    email = request.session.get('email', None)
    
    # Render the feedback form page with the pet details
    return render(request, "dog_feedback.html", {
        'j': pet.breed,
        'd': pet.age,
        'e': pet.dogname,
        'm': email,
    })

def dog_feed(request):
    if request.method == 'POST':
        # Extract data from POST request
        email = request.POST.get('email') or request.session.get('email')
        
        # Ensure email exists
        if not email:
            return render(request, 'dog_feedback.html', {'error': 'Email is required'})

        # Save the feedback to the Dog_feedback model
        feedback = Dog_feddback.objects.create(
            age=int(request.POST.get('age')),
            dogname=request.POST.get('dogname'),
            breed=request.POST.get('breed'),
            image=request.FILES.get('image'),
            feedback_text=request.POST.get('feedback_text'),
            rating=request.POST.get('rating')
        )
        
        # Redirect to the user home page after submission
        return redirect('user_home')
    
    return render(request, 'dog_feedback.html')



#donation

from datetime import datetime

def add_donate(request):
    email = request.session.get('email')
    if email:
        user = user_reg.objects.get(email=email)  
        if request.method == 'POST':
            name = request.POST.get('name')
            idproof = request.POST.get('idproof')
            phno = request.POST.get('phno')
            price = request.POST.get('price')
            current_date = datetime.now().strftime('%Y-%m-%d')  # Format as required
            Donation_amount.objects.create(
                name=name, idproof=idproof, phno=phno, email=email, price=price, date=current_date
            )
            return redirect('complete_donation')
        return render(request, 'add_donate.html', {'user': user}) 
    return redirect('login')  


def complete_donation(request):
    email = request.session.get('email')
    if email:
        c=Donation_amount.objects.get(email=email)
        return render(request,'complete_donation.html',{'d':c})
    return render(request,'complete_donation.html')

def payment(request,id):
    email = request.session['email']
    user = user_reg.objects.get(email=email)
    donate = Donation_amount.objects.get(id=id)

    
    calculated_price = donate.price 

    
    Pay(
        idproof=user.idproof,
        phno=user.phno,
        price=calculated_price,
        email=user.email,
        date=datetime.now().date(),
         
    ).save()
    donate.delete()


    totalprice = int(calculated_price * 100)  # Convert to paise
    currency = 'INR'

    # Create Razorpay order
    razorpay_order = razorpay_client.order.create(dict(amount=totalprice, currency=currency, payment_capture='0'))
    razorpay_order_id = razorpay_order['id']
    callback_url = '/paymenthandler/'

    context = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': totalprice,
        'currency': currency,
        'callback_url': callback_url,
    }

    return render(request, 'payment.html', context=context)


@csrf_exempt
def paymenthandler(request):

    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is not None:
                amount = 20000
                try:
                    razorpay_client.payment.capture(payment_id, amount)
                    return render(request, 'pay_success.html')
                except:
                    return render(request, 'pay_failed.html')
            else:
                return render(request, 'pay_failed.html')
        except Exception as e:
            return render(request, 'user_home.html')
    else:
        return render(request, 'user_home.html')



#muncipalitylogin
def muncipalitylogin(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        cr=models.Muncipality.objects.filter(username=username,password=password)
        if cr:
            userd=models.Muncipality.objects.get(username=username,password=password)
            id=userd.id
            username=userd.username
            password=userd.password
            request.session['id']=id
            request.session['username']=username
            request.session['password']=password
            return redirect('muncipalityhome')
        else:
            msg = 'invalid password or username'
            return render(request,'muncipalitylogin.html', {'msg':msg})
    return render(request,'muncipalitylogin.html') 

def muncipalityhome(request):
    return render(request,'muncipalityhome.html')    

#muncipalityaddpet
def add_pet(request):
    muncipality_name = request.session.get('username')  
    if muncipality_name:
        m = models.Muncipality.objects.filter(username=muncipality_name).first()
        if not m:
            return HttpResponse("Municipality with this email does not exist.")
        
    if request.method == 'POST':
        dogname = request.POST.get('dogname')
        age = request.POST.get('age')
        breed = request.POST.get('breed')
        image = request.FILES.get('image')
        color = request.POST.get('color')
        gender = request.POST.get('gender')

        if models.Pet.objects.filter(dogname=dogname).exists():
            alert_message = "<script>alert('THIS DOG ALREADY EXISTS');window.location.href='/add_pet/';</script>"
            return HttpResponse(alert_message)

        pet = models.Pet(dogname=dogname, age=age, breed=breed, image=image, color=color,gender=gender, muncipality=m)
        pet.save()

        return redirect('list_dogs')  

    return render(request, 'add_pet.html', {'a': m})

def list_dogs(request):
    muncipality_name = request.session.get('username')
    if muncipality_name:
        muncipality = Muncipality.objects.filter(username=muncipality_name).first()
        if not muncipality:
            return render(request, 'muncipality_login.html')

        pets = Pet.objects.filter(muncipality=muncipality)  # Use the foreign key to filter pets
        return render(request, 'list_dogs.html', {'p': pets})
        
    return render(request, 'muncipality_login.html')

def update_pet_status(request, pet_id):
    if request.method == 'POST':
        pet = get_object_or_404(Pet, id=pet_id)
        pet.status = request.POST.get('status')
        pet.save()
        return redirect('list_dogs')  

def list_feedback(request, id):
    feedback = Dog_feddback.objects.get(id=id)
    try:
        rating = int(feedback.rating)
    except ValueError:
        rating = 0 
    range_value = range(rating)
    return render(request, 'list_feedback.html', {'f': feedback, 'range_value': range_value})



def delete_dogs(request,id):
    pet =Pet.objects.get(id=id)
    pet.delete()
    return redirect('list_dogs')



def list_adoption(request):
    muncipality_name = request.session.get('username')
    if muncipality_name:
        muncipality = get_object_or_404(Muncipality, username=muncipality_name)
        print(f"Retrieved Municipality: {muncipality}")
        adoptions = Adopt.objects.filter(muncipality_name=muncipality)
        print(f"Number of adoptions found: {adoptions.count()}")
        for adoption in adoptions:
            print(f"Dog Name: {adoption.dogname}, Breed: {adoption.breed}, Age: {adoption.age}")
        return render(request, 'list_adoption.html', {'adoptions': adoptions})
    print("No municipality name found in session.")
    return render(request, 'list_adoption.html')





 
#addtrainer

def trainerreg(request):
    muncipality_name = request.session.get('username')
    if muncipality_name:
        m = Muncipality.objects.filter(username=muncipality_name).first()
        if not m:
            return HttpResponse("Municipality with this email does not exist.")
        
        if request.method == 'POST':  
            Name = request.POST.get('Name')
            place = request.POST.get('place')
            address = request.POST.get('address')
            gender = request.POST.get('gender')
            email = request.POST.get('email') 
            certificate = request.FILES.get('certificate')
            phno = request.POST.get('phno')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            image = request.FILES.get('image')

            if password != confirm_password:
                msg = "Passwords do not match"
                return render(request, 'trainerreg.html', {'msg': msg})

            if trainer_reg.objects.filter(email=email).exists():
                alert_message = "<script>alert('EMAIL ALREADY EXISTS');window.location.href='/trainer_register/';</script>"
                return HttpResponse(alert_message)
        
            trainer_reg.objects.create(
                Name=Name, place=place, email=email, phno=phno,
                certificate=certificate, password=password,confirm_password=confirm_password, image=image, 
                address=address, gender=gender, muncipality=m
            )
            return redirect('muncipalityhome')
        
        return render(request, 'trainerreg.html', {'a': m})
    
    return render(request, 'muncipality_login.html')



#muncipalitytrainerlist

from django.shortcuts import render
from shop.models import trainer_reg, Muncipality

def list_trainer(request):
   muncipality = request.session.get('username')
   if muncipality:
        muncipality = get_object_or_404(Muncipality, username=muncipality)
        print(f"Retrieved Municipality: {muncipality}")
        t = trainer_reg.objects.filter(muncipality=muncipality)
        return render(request, 'list_trainer.html', {'trainers': t})
   else:
        print("No muncipality name found in session.")
        # If the session does not have a muncipality name, redirect to the login page
        return render(request, 'muncipalitylogin.html')





#delete_trainers

def delete_trainer(request,id):
    trainer = trainer_reg.objects.get(id=id)
    trainer.delete()
    return redirect('list_trainer')



#edittrainer


def edittrainer(request, id):
    muncipality_name = request.session.get('username')
    if muncipality_name:
        m = models.Muncipality.objects.filter(username=muncipality_name).first()
        if not m:
            return HttpResponse("Muncipality with this email does not exist.")
    trainer = get_object_or_404(trainer_reg, id=id)
    
    if request.method == 'POST':
        trainer.Name = request.POST.get('Name')
        trainer.place = request.POST.get('place')
        trainer.address = request.POST.get('address')
        trainer.gender = request.POST.get('gender')
        
        trainer.email = request.POST.get('email')
        trainer.muncipality_name = muncipality_name  # Set from session
        trainer.phno = request.POST.get('phno')
        trainer.password = request.POST.get('password')
        if trainer.certificate is not None:
            trainer.certificate = trainer.certificate
        trainer.save()
        return redirect('muncipalityhome')

    places = ["Kollam", "Kottayam", "Thiruvananthapuram", "Ernakulam", "Alappuzha", "Iddukki", "Palakad", "Thirssur", "Pathanamthitta"]

    return render(request, 'edittrainer.html', {'t': trainer, 'm': m, 'places': places})

#assignwork


def addwork(request, trainer_id):
    muncipality_name = request.session.get('username')
    if muncipality_name:
        m = models.Muncipality.objects.filter(username=muncipality_name).first()
    trainer = trainer_reg.objects.get(id=trainer_id)
    if request.method == "POST":
        
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        location = request.POST.get('location')
        details = request.POST.get('details')
        

        Timetable.objects.create(
            trainer=trainer,
            muncipality_name=muncipality_name,
            date=date,
            start_time=start_time,
            end_time=end_time,
            location=location,
            details=details
            
        )

        return redirect('list_work') 

    return render(request, 'addwork.html', {'t': trainer,'a':m})




def confirmwork(request,trainer_id):
    data=Timetable.objects.select_related('trainer').get(id=trainer_id)
    emaill=data.trainer.email
    print('email address',emaill)
    print(emaill)
    data.is_accepted = True
    data.save()
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("aiswaryajobe2002@gmail.com", "eekr kdxe dxcn zfnq")
    message = 'Work posted successfully'
    s.sendmail("aiswaryajobe2002@gmail.com",emaill,message)
    s.quit()
    return redirect('list_trainer')

def list_work(request):
    muncipality_name =  request.session.get('username')
    if muncipality_name:
        t = Timetable.objects.select_related('trainer').filter(muncipality_name=muncipality_name)  
        return render(request, 'list_work.html', {'w': t})
    return render(request, 'list_work.html', {'w': t})

#vaccine 
def addvaccination(request, dog_id):
    muncipality_name = request.session.get('username')
    if muncipality_name:
        m = models.Muncipality.objects.filter(username=muncipality_name).first()
    dog = Pet.objects.get(id=dog_id)
    if request.method == "POST":
        date = request.POST.get('date')
        batchnumber = request.POST.get('batchnumber')
        due = request.POST.get('due')
        veterinarian = request.FILES.get('veterinarian')
        
        Vaccinations.objects.create(
            dog=dog,
            muncipality_name=muncipality_name,
            date=date,
            batchnumber=batchnumber,
            due=due,
            veterinarian=veterinarian,
        )

        return redirect('list_dogs') 

    return render(request, 'addvaccination.html', {'t': dog,'a':m})

def user_addvaccination(request,id):
    dog = Adopt.objects.get(id=id)
    if request.method == "POST":
        date = request.POST.get('date')
        batchnumber = request.POST.get('batchnumber')
        due = request.POST.get('due')
        veterinarian = request.FILES.get('veterinarian')
        
        Vaccinations(
            dog=dog,
            date=date,
            batchnumber=batchnumber,
            due=due,
            veterinarian=veterinarian,
        ).save()

        return redirect('user_adopt') 

    return render(request, 'user_addvaccination.html', {'t': dog})



def vaccine_list(request,dog_id):
    vaccinations = Vaccinations.objects.select_related('dog').filter(dog_id=dog_id)
    return render(request, 'vaccine_list.html', {'v': vaccinations})

#trainerlogin
def trainerlog(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        cr=trainer_reg.objects.filter(email=email,password=password)
        if cr:
            userd=models.trainer_reg.objects.get(email=email,password=password)
            id=userd.id
            email=userd.email
            password=userd.password
            request.session['id']=id
            request.session['email']=email
            request.session['password']=password
            return redirect('trainerhome')
        else:
            msg = 'invalid password or email'
            return render(request,'trainerlog.html', {'msg':msg})
    return render(request,'trainerlog.html')  


def trainerhome(request):
    return render(request,'trainerhome.html')

#trainerprofile
def trainer(request):
    email = request.session.get('email')
    if not email:
        return render(request, 'user_home.html', {'error': 'User not logged in'})
    tr = get_object_or_404(trainer_reg, email=email)

    user_info = {
        'Name': tr.Name,
        'gender':tr.gender,
        'place':tr.place,
        'address':tr.address,       
        'phno': tr.phno,
        'email': tr.email,
        'certificate':tr.certificate,
        'password': tr.password,
        'confirm_password': tr.confirm_password,
        'image': tr.image
    }
    
    return render(request, 'trainer_profile.html', user_info)

#trainerprofileupdation
def trainerupdate_profile(request):
    email=request.session['email']
    cr =trainer_reg.objects.get(email=email)
    if cr:
        user_info = {
            'Name':cr.Name,
            'gender': cr.gender,
            'place':cr.place,
            'address':cr.address,
            'phno':cr.phno,
            'email':cr.email,
            'password':cr.password,
            'certificate':cr.certificate,
            'confirm_password':cr.confirm_password,
            'image':cr.image,
            
        }
        return render(request,'trainerupdate_profile.html',user_info)
    else:
        return render(request,'trainerupdate_profile.html')  
    
def newupdate(request):
    email = request.session.get('email')
    if not email:
        return redirect('trainer_login') 
    if request.method == "POST":
        user = trainer_reg.objects.get(email=email)
        Name = request.POST.get('Name')
        gender = request.POST.get('gender')
        place= request.POST.get('place')
        address= request.POST.get('address')
        phno = request.POST.get('phno')
        certificate = request.FILES.get('certificate')
        confirm_password = request.POST.get('confirm_password')
        image = request.FILES.get('image')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user.Name = Name
        user.gender = gender
        user.phno = phno
        user.place = place
        user.certificate = certificate
        user.confirm_password = confirm_password
        user.email = email
        user.password = password
        user.address = address
        
        if image:
            user.image = image

        if certificate:
            user.certificate = certificate    

        
        user.save()
        
        user_info = {
            'Name': user.Name,
            'gender': user.gender,
            'address':user.address,
            'phno': user.phno,
            'place': user.place,
            'certificate': user.certificate,
            'confirm_password': user.confirm_password,
            'phno': user.phno,
            'email': user.email,
            'password': user.password,
            'image': user.image,
        }
        
        return render(request, 'trainer_profile.html', user_info)
    else:
        return render(request, 'trainerupdate_profile.html') 



#worklist
def worklist(request):
    email = request.session.get('email')
    if email:
        t = Timetable.objects.filter(trainer__email=email)
        return render(request, 'worklist.html', {'w': t})
    return render(request,'worklist.html')  


#admintrainerlist
def trainer_list(request):
    t=trainer_reg.objects.all()
    return render(request,'trainers.html',{'trainers':t}) 

from . models import Admin

def adminreg(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        Admin(username=username, password=password).save()
        return redirect('adminlogin')
    return render(request,'adminreg.html')

#adminlogin
def adminlogin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        cr=Admin.objects.filter(username=username,password=password)
        if cr:
                a=Admin.objects.get(username=username,password=password)
                username=a.username
                password=a.password
                id=a.id
                request.session['username']=username
                request.session['id']=id
                return render(request,'adminhome.html')   
    return render(request,'adminlogin.html')
    
def adminhome(request):
    return render(request,'adminhome.html') 

#adminaddmuncipality

def add_muncipality(request):
    if request.method == 'POST':
        muncipality_name = request.POST['muncipality_name']
        place = request.POST['place']
        phone = request.POST['phone']
        muncipality_email = request.POST['muncipality_email']
        username = request.POST['username']
        password = request.POST['password']

        
        muncipality = models.Muncipality(
            muncipality_name=muncipality_name,
            place=place,
            phone=phone,
            muncipality_email=muncipality_email,
            username=username,
            password=password
        )
        muncipality.save()

        return redirect('adminhome') 
    return render(request, 'addmuncipality.html')




def muncipalitylist(request):
    m=models.Muncipality.objects.all()
    return render(request,'muncipalitylist.html',{'m':m})

def deletemuncipality(request,id):
    m = models.Muncipality.objects.get(id=id)
    m.delete()
    return redirect('muncipalitylist')

def adopt_list(request):
    adoptions = Adopt.objects.all()
    return render(request, 'adopt_list.html', {'adoptions': adoptions})



def donation_list(request):
    d = Pay.objects.all()  
    return render(request, 'donation_list.html', {'donate': d})



from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from .models import user_reg

def request_password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = user_reg.objects.get(email=email)
        except user_reg.DoesNotExist:
            messages.error(request, 'No user with this email exists.')
            return redirect('request_password_reset')

        # Generate token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.id))

        # Create reset link
        reset_link = request.build_absolute_uri(
            f'/reset_password/{uid}/{token}/'
        )

        # Send email
        subject = 'Password Reset Request'
        message = render_to_string('password_reset_email.html', {
            'user': user,
            'reset_link': reset_link,
        })
        send_mail(subject, message, 'aiswaryajobe2002@gmail.com', [email])

        messages.success(request, 'Password reset email sent!')
        return redirect('userlogin')

    return render(request, 'request_password_reset.html')

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode

def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = user_reg.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, user_reg.DoesNotExist):
        user = None

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        new_confirm_password = request.POST.get('new_confirm_password')

        if new_password == new_confirm_password:
            user.password = new_password  # Ideally, hash the password
            user.save()
            messages.success(request, 'Your password has been reset successfully!')
            return redirect('userlogin')
        else:
            messages.error(request, 'Passwords do not match.')

    return render(request, 'reset_password.html', {'user': user, 'token': token})
