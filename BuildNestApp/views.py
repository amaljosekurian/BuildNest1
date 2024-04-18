from django.contrib.auth import login, authenticate,get_user_model
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .models import *
from django.views.decorators.cache import never_cache
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt


#@never_cache
def index(request):
    return render(request, "index.html")

#@login_required
def index2(request):
    if 'email' in request.session:
       response = render(request, 'index2.html')
       response['Cache-Control'] = 'no-store, must-revalidate'
       return response
    else:
       return redirect('index')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        role = request.POST['role']
        firstname = request.POST['fname']
        email = request.POST['email']
        lastname = request.POST['lname']
        password = request.POST['password']
        phone = request.POST['phone']

        user = Usertable(first_name=firstname, last_name=lastname, email=email, phone=phone, username=username)
        user.set_password(password)
        
        if role == 'Contractor_user':
            user.is_contractor = True
        elif role == 'Client_user':
            user.is_client = True
        elif role == 'Purchase_manager':
            user.is_purchase_manager = True
        elif role == "Engineer":
            user.is_engineer = True
        
        user.save()
        return redirect('login')
        # return HttpResponse(role)

    return render(request, "signup.html")

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if user.is_client:
                return redirect("client")
            elif user.is_contractor:
                return redirect("contractor")
            elif user.is_admin:
                return redirect("adminreg")
            elif user.is_purchase_manager:
                return redirect("purchase_manager")
            elif user.is_engineer:
                return redirect('engineerIndex')
            else:
                return HttpResponse("Not Found")
        else:
            return HttpResponse('User Not Avail')
    else:
        return render(request, 'login.html')



def adminreg(request):
    if request.method == 'POST':
        # return HttpResponse('Done')
        for user in Usertable.objects.exclude(is_admin=True):
            status_field_name = f'user_status_{user.email}'
            user_status = request.POST.get(status_field_name, '')  # Get the value of the checkbox

            if user_status == 'on':
                # If the checkbox is checked, activate the user
                if not user.is_active:
                    user.is_active = True
                    user.save()
                    send_activation_email(user)  # Send an email for activation
            else:
                # If the checkbox is not checked, deactivate the user
                if user.is_active:
                    user.is_active = False
                    user.save()
                    send_deactivation_email(user)  # Send an email for deactivation
    else:
        # Retrieve users based on their roles for the GET request
        admin_users = Usertable.objects.filter(is_admin=True)
        Purchase_manager = Usertable.objects.filter(is_purchase_manager=True)
        Client_user = Usertable.objects.filter(is_client=True)
        Contractor_user = Usertable.objects.filter(is_contractor=True)
        engineer_user = Usertable.objects.filter(is_engineer=True)

        context = {
            'admin_users': admin_users,
            'Purchase_manager': Purchase_manager,
            'Client_user': Client_user,
            'Contractor_user': Contractor_user,
            'engineers': engineer_user
        }

        return render(request, 'adminreg.html', context)
    
def UserAcivation(requset, id):
    guestUser = Usertable.objects.get(id = id)
    if (guestUser.is_active):
        guestUser.is_active = False
        send_deactivation_email(guestUser)
    else:
        guestUser.is_active = True
        send_activation_email(guestUser)
    guestUser.save()
    return redirect('adminreg')


def logout(request):
    auth_logout(request)
    return redirect('index')

def toggle_active(request, user_id, is_active):
    try:
        user = Usertable.objects.get(id=user_id)
        # Convert the "is_active" parameter to a boolean
        is_active = is_active.lower() == 'true'
        # Toggle the active status
        user.is_active = not is_active
        user.save()
        messages.success(request, f'User is now {"Active" if user.is_active else "Inactive"}.')
    except Usertable.DoesNotExist:
        messages.error(request, 'User not found.')
    return redirect('admind')  # Replace 'admind' with your actual admin dashboard URL name


def user_profile(request):
    user = request.user
    context = {'user': user}
    return render(request, 'user_profile.html', context)


def update_user_details(request):
    if request.method == 'POST':
        new_first_name = request.POST.get('new_first_name')
        new_last_name = request.POST.get('new_last_name')
        new_phone_number = request.POST.get('new_phone_number')  # Add this line

        # Update the user's details in the database
        user = request.user
        user.first_name = new_first_name
        user.last_name = new_last_name
        user.phone = new_phone_number  # Add this line
        user.save()

        messages.success(request, 'User details updated successfully.')
        return redirect('user_profile')  # Redirect to the user profile page

    return render(request, 'user_profile')

# @login_required
def contractor(request):
    client_requests = PlotData.objects.filter(Q(contractor__isnull=True)&Q(plan_pdf__isnull=False))
    data = {
        "contracts": client_requests
    }
    return render(request, 'contractor.html', data)
def construction_sites(request):
    # Retrieve construction sites for the logged-in user
    construction_sites = ConstructionSite.objects.filter(user=request.user)
    return render(request, 'construction_sites.html', {'construction_sites': construction_sites})
from django.http import JsonResponse
from .models import ConstructionSite, Product

from django.http import JsonResponse
from .models import ConstructionSiteAssociation

def get_product_details(request):
    site_id = request.GET.get('site_id')
    products = ConstructionSiteAssociation.objects.filter(construction_site_id=site_id).select_related('product')
    
    product_details = []
    for association in products:
        product = association.product
        product_detail = {
            'category': product.category,
            'brand_name': product.brand_name,
            # 'color': product.color,
            # 'stocks': product.stocks,
            'product_description': product.product_description,
            # 'price_per_unit': product.price_per_unit,
            # 'price': product.price,
            'thumbnail': product.thumbnail.url  # Assuming thumbnail is a FileField
        }
        product_details.append(product_detail)

    return JsonResponse(product_details, safe=False)


# @login_required
def client(request):
    projects = PlotData.objects.filter(Q(payment_request=True))
    data = {
        "projects": projects
    }
    return render(request, 'client.html', data)

# def purchase_manager(request):
#     categories = Product.objects.values_list('category', flat=True).distinct()
#     products = Product.objects.all()
#     return render(request, 'purchase_manager.html', {'categories': categories, 'products': products})



from django.shortcuts import render
from .models import Product

def purchase_manager(request):
    # Get distinct categories
    categories = Product.objects.values_list('category', flat=True).distinct()

    # Apply search filter
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(
            models.Q(category__icontains=query) |
            models.Q(brand_name__icontains=query) |
            models.Q(color__icontains=query) |
            models.Q(product_description__icontains=query)
        )
    else:
        products = Product.objects.all()

    # Apply category filter
    selected_category = request.GET.get('category')
    if selected_category:
        products = products.filter(category=selected_category)

    # Apply brand name filter
    selected_brand = request.GET.get('brand')
    if selected_brand:
        products = products.filter(brand_name=selected_brand)

    return render(request, 'purchase_manager.html', {
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
        'selected_brand': selected_brand,
        'search_query': query,
    })

def send_activation_email(user):
    send_mail(
        'Account Activation',
        'Your account has been activated. You can now log in and access your account.',
        'buildnest97@gmail.com',  # Replace with your email address
        [user.email],
        fail_silently=False,
    )

def send_deactivation_email(user):
    send_mail(
        'Account Deactivation',
        'Your account has been deactivated. Please contact the admin for more information.',
        'buildnest97@gmail.com',  # Replace with your email address
        [user.email],
        fail_silently=False,
    )

# def delAdmin(request):
#     id=3
#     Usertable.objects.get(id=id).delete()
#     return HttpResponse('Successfully Deleted')

def sitereg(request):
    # Your view logic here, if needed
    return render(request, 'sitereg.html')

@login_required
def requestContract(request):
    if request.method == 'POST':
        apprx_Budget = request.POST['approximate_budget']
        plot_address = request.POST['plot_address']
        plot_id_document = request.FILES['plot_id_document']
        plot_images = request.FILES.getlist('plot_images')
        plot_location = request.POST['plot_location']
        square_feet = request.POST['square_feet']
        plotbasicdata = PlotBasicData()
        plotimages = PlotImages()
        plotdata = PlotData()
        plotdata.plot_user = Usertable.objects.get(id=request.user.id)
        plotbasicdata.approximate_budget = apprx_Budget
        plotbasicdata.plot_address = plot_address
        plotbasicdata.plot_id_document = plot_id_document
        plotbasicdata.plot_location = plot_location
        plotbasicdata.square_feet = square_feet
        plotbasicdata.save()
        plotdata.plotBaseData = plotbasicdata
        plotdata.save()
        for image in plot_images:
                PlotImages.objects.create(plot=plotdata, plot_images=image)
        request.session["projectID"] = plotdata.id
        return redirect('requestContract2')
        # return HttpResponse(request.user)
    else:
        # PlotBasicData.objects.all().delete()
        # PlotData.objects.all().delete()
        return render(request, 'contractRequest.html')

def requestContract2(request):
    if request.method == 'POST':
        # Handle form submission
        num_floors = request.POST.get('num_floors')
        work_area_required = request.POST.get('work_area_required') == 'yes'
        store_room_required = request.POST.get('store_room_required') == 'yes'
        dining_room_required = request.POST.get('dining_room_required') == 'yes'
        kitchen_type = request.POST.get('kitchen_type')
        additional_amenities = request.POST.get('additional_amenities', '')
        engineerSelected = request.POST.get('engineer')

        project_details = ProjectData.objects.create(
            num_floors=num_floors,
            work_area_required=work_area_required,
            store_room_required=store_room_required,
            dining_room_required=dining_room_required,
            kitchen_type=kitchen_type,
            additional_amenities=additional_amenities
        )

        # Create floor details
        for floor_number in range(1, int(num_floors) + 1):
            num_rooms = request.POST.get(f'floor{floor_number}_rooms')
            num_bathrooms = request.POST.get(f'floor{floor_number}_bathrooms')

            FloorDetails.objects.create(
                project=project_details,
                floor_number=floor_number,
                num_rooms=num_rooms,
                num_bathrooms=num_bathrooms
            )
        plot = PlotData.objects.get(id=request.session['projectID'])
        plot.engineer = Usertable.objects.get(id=engineerSelected)
        plot.projectdata = project_details
        plot.save()
        return redirect('succesfullContract')
    else:    
        # ProjectData.objects.all().delete()
        # return HttpResponse(request.session['projectID'])
        data = {
            "engineer": Usertable.objects.filter(is_engineer=True)
        }
        return render(request, 'contractRequest2.html', data)
    
def SuccessView(request):
    return render(request, 'succesfullContract.html')


from django.db.models import Q
@login_required
def EngineerIndex(request): 
    data = {
        "projects": False,
        "approvedPo": False
    }
    
    
    if PlotData.objects.filter(Q(engineer_id=request.user.id)&Q(payment_is_Done=False)&Q(plan_pdf__isnull=False)):
        data['projects'] = PlotData.objects.filter(Q(engineer_id=request.user.id)&Q(payment_request=False)&Q(payment_is_Done=False))
    if PlotData.objects.filter(Q(engineer_id=request.user.id)&Q(payment_is_Done=True)):
        data['approvedPo'] = PlotData.objects.filter(Q(engineer_id=request.user.id)&Q(payment_request=False)&Q(payment_is_Done=True))
        
    return render(request, "engineerIndex.html", data)


def ProjectExplorer(request, id):
    projectC = PlotData.objects.get(id=id)
    data = {
        "projectC": projectC,
        "floorData": FloorDetails.objects.filter(project=projectC.projectdata),
        "plotImages": PlotImages.objects.filter(plot=projectC)
    }
    return render(request, "projectExplorer.html", data)

def createFeeToken(request, id):
    projectSel = PlotData.objects.get(id=id)
    projectSel.payment_request = True
    projectSel.plan_fee = request.POST['feeRe']
    projectSel.save()
    return redirect('engineerIndex')

def projectplanUpdate(request, id):
    if request.method == 'FILES':
        plotdata = PlotData.objects.get(id=id)
        myfile = request.FILES.get('pdf_file')
        if myfile:
            plotdata.plan_pdf = myfile
        plotdata.save()
    return redirect('engineerIndex')

import razorpay
def planBillPayment(request, id):
    projectX = PlotData.objects.get(id=id)
    client = razorpay.Client(auth=("rzp_test_FX0zShFTZ38jpg", "hfq4cuzgZs7CqhvBhg5NBRNG"))
    payment = client.order.create({'amount': "400000",'currency':'INR','payment_capture':'1'})
    data = { "amount": 1000, "currency": "INR", "receipt": "order_rcptid_11", "payment":payment, "projectx": projectX }
    return render(request, "planBillPayment.html", data) 

@csrf_exempt
def successPage(request):
    print(request.POST)
    plotId = request.POST['plotdataid']
    plot = PlotData.objects.get(id=plotId)
    plot.payment_is_Done = True
    plot.payment_request = False
    plot.save()
    return redirect('client')



def add_site(request):
    return render(request, 'add_site.html')



@login_required
def add_construction_site(request):
    if request.method == 'POST':
        site_name = request.POST.get('site_name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        upload_permits = request.FILES.get('upload_permits')
        approximate_budget = request.POST.get('approximate_budget')
        additional_description = request.POST.get('additional_description')
        site_location = request.POST.get('site_location')

        # Get the currently logged in user
        user = request.user

        # Create ConstructionSite object and save to database
        new_site = ConstructionSite.objects.create(
            site_name=site_name,
            start_date=start_date,
            end_date=end_date,
            upload_permits=upload_permits,
            approximate_budget=approximate_budget,
            additional_description=additional_description,
            site_location=site_location,
            user=user
        )
        # Redirect to a success page or any other page as needed
        # return redirect('success_page_url')

    return render(request, 'add_site.html')

def workers(request):
    if request.method == 'POST':
        # Process form submission
        for worker in Worker.objects.all():
            salary_frequency = request.POST.get(f'salary_frequency_{worker.pk}')
            salary_amount = request.POST.get(f'salary_amount_{worker.pk}')
            worker.salary_frequency = salary_frequency
            worker.salary_amount = salary_amount
            worker.save()
        return redirect('add_worker')  # Redirect to the same page after submission
    else:
        # Fetch all workers from the database
        workers = Worker.objects.all()
        return render(request, 'view_worker.html', {'workers': workers})
    


from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Worker, ConstructionSite  # Assuming you have a Worker model and ConstructionSite model
from twilio.rest import Client

def send_sms_message(from_number, to_number, message):
    # Twilio credentials
    account_sid = 'AC8623cf11fecb7f92521d956000182b18'
    auth_token = '2c4f900447b0040b4bffacb4e366b238'

    # Initialize Twilio client
    client = Client(account_sid, auth_token)

    try:
        # Send WhatsApp message
        message = client.messages.create(
            body=message,
            from_=from_number,  # Your Twilio phone number
            to=to_number  # Recipient's phone number
        )
        return True, message.sid
    except Exception as e:
        print(f"Failed to send message: {e}")
        return False, None

def add_worker(request):
    if request.method == 'POST':
        # Extract data from the request
        name = request.POST.get('name')
        job_role = request.POST.get('job_role')
        state = request.POST.get('state')
        district = request.POST.get('district')
        mobile_number = request.POST.get('mobile_number')
        aadhar_document = request.FILES.get('aadhar_document')
        site_id = request.POST.get('construction_site')  # Get the selected site ID

        # Ensure user is authenticated
        if request.user.is_authenticated:
            user_id = request.user.id

            # Create and save a new Worker instance
            worker = Worker(
                name=name,
                job_role=job_role,
                state=state,
                district=district,
                mobile_number=mobile_number,
                aadhar_document=aadhar_document,
                user_id=user_id,
                site_id=site_id  # Assign the selected site ID
            )
            worker.save()
            
            from_number = '+12513021610'
            success, message_id = send_sms_message(from_number, mobile_number, 'Worker added successfully.')

            if success:
                return JsonResponse({'success': True, 'message': 'Worker added successfully.', 'message_id': message_id})
            else:
                return JsonResponse({'success': False, 'message': 'Failed to send message.'})
        else:
            # Handle unauthenticated user
            return HttpResponse("User is not authenticated")
    else:
        # If the request method is not POST, render the form
        construction_sites = ConstructionSite.objects.all()  # Query all construction sites
        return render(request, 'add_worker.html', {'construction_sites': construction_sites})

from django.shortcuts import render

def warehouse_home(request):
    return render(request, 'warehouse_home.html')

from .models import Product

def add_product(request):
    categories = Category.objects.all()  
    
    
    if request.method == 'POST':
        category = request.POST.get('category')
        product_name = request.POST.get('productName')
        brand_name = request.POST.get('brandName')
        color = request.POST.get('color', '')  # Color is optional, so use get() with a default value
        stocks = request.POST.get('stocks')
        product_description = request.POST.get('productDescription')
        thumbnail = request.FILES.get('thumbnail')
        price_per_unit = request.POST.get('pricePerUnit')
        price = request.POST.get('price')
        
        # Save the product to the database
        product = Product(
            category=category,
            product_name = product_name,
            brand_name=brand_name,
            color=color,
            stocks=stocks,
            product_description=product_description,
            thumbnail=thumbnail,
            price_per_unit=price_per_unit,
            price=price
        )
        product.save()
        
        return redirect('add_product')  # Assuming you have a URL named 'product_list' for listing products
    
    return render(request, 'add_product.html', {'categories': categories})  # Pass categories to the template context


# views.py

from django.shortcuts import redirect
from .models import CartItem

def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(pk=product_id)  # Assuming you have a Product model
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
        )
        if not created:
            cart_item.save()
    return redirect('purchase_manager')  # Redirect to the cart page

def view_cart(request):
    user = request.user  # Assuming you have authentication enabled
    cart_items = CartItem.objects.filter(user=user)
    construction_sites = ConstructionSite.objects.all()  # Fetch all construction sites
    return render(request, 'cart.html', {'cart_items': cart_items, 'construction_sites': construction_sites})


from django.shortcuts import redirect, get_object_or_404
from .models import CartItem

def remove_from_cart(request, item_id):
    if request.method == 'POST':
        # Get the cart item
        cart_item = get_object_or_404(CartItem, pk=item_id)

        # Delete the cart item
        cart_item.delete()

    return redirect('view_cart')  # Redirect to the cart page

def add_to_site(request):
    if request.method == 'POST':
        construction_site_id = request.POST.get('construction_site')
        construction_site = ConstructionSite.objects.get(id=construction_site_id)
        user = request.user
        cart_items = CartItem.objects.filter(user=user)
        for item in cart_items:
            ConstructionSiteAssociation.objects.create(construction_site=construction_site, product=item.product, user=user)
    return redirect('add_product')  # Redirect to home page if the request method is not POST

def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        if category_name:
            Category.objects.create(name=category_name)
            return redirect('add_category')  # Redirect to some view after adding category
    return render(request, 'add_category.html')