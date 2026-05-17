VERSION 5.00
Begin VB.Form Form1 
   BackColor       =   &H00400000&
   BorderStyle     =   0  'None
   Caption         =   "Form1"
   ClientHeight    =   5490
   ClientLeft      =   0
   ClientTop       =   0
   ClientWidth     =   7350
   LinkTopic       =   "Form1"
   ScaleHeight     =   5490
   ScaleWidth      =   7350
   ShowInTaskbar   =   0   'False
   StartUpPosition =   2  'CenterScreen
   Begin VB.Timer Timer2 
      Interval        =   750
      Left            =   0
      Top             =   4440
   End
   Begin VB.Timer Timer1 
      Interval        =   1500
      Left            =   0
      Top             =   4920
   End
   Begin VB.Label Update 
      BackStyle       =   0  'Transparent
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   12
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H00FFFFFF&
      Height          =   735
      Left            =   480
      TabIndex        =   4
      Top             =   4680
      Width           =   6735
   End
   Begin VB.Label Label4 
      AutoSize        =   -1  'True
      BackStyle       =   0  'Transparent
      Caption         =   "A Hurdle's Mom Inc. Intl. production"
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   12
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H00FFFFFF&
      Height          =   300
      Left            =   2160
      TabIndex        =   3
      Top             =   960
      Width           =   4320
   End
   Begin VB.Label Label3 
      AutoSize        =   -1  'True
      BackStyle       =   0  'Transparent
      Caption         =   "Presents:"
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   12
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H00FFFFFF&
      Height          =   300
      Left            =   840
      TabIndex        =   2
      Top             =   960
      Width           =   1155
   End
   Begin VB.Image Image1 
      Height          =   3120
      Left            =   2280
      Stretch         =   -1  'True
      Top             =   1320
      Width           =   2640
   End
   Begin VB.Label Label2 
      AutoSize        =   -1  'True
      BackStyle       =   0  'Transparent
      Caption         =   "Hurdle's Mom Inc. Intl."
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   24
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H00FFFFFF&
      Height          =   555
      Left            =   1080
      TabIndex        =   1
      Top             =   360
      Width           =   5115
   End
   Begin VB.Label Label1 
      AutoSize        =   -1  'True
      BackStyle       =   0  'Transparent
      Caption         =   "Hurdle's Mom Inc. Intl."
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   24
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H000000C0&
      Height          =   555
      Left            =   1080
      TabIndex        =   0
      Top             =   360
      Width           =   5115
   End
End
Attribute VB_Name = "Form1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Dim intCredit As Integer
Dim intCurrent As Integer
Dim strarrCredits(25) As String
Dim strarrIcon(17) As String

Private Sub Form_Click()
    Unload Me
    Unload frmForm
End Sub

Private Sub Form_Load()
    Randomize
    Image1.Picture = LoadPicture(App.Path & "\Icons\tree.bmp")
    
    Label2.Left = Label1.Left - 10
    Label2.Top = Label1.Top + 10
    Label1.ZOrder
    
    strarrCredits(1) = "President: Senior Airman"
    strarrCredits(2) = "CEO: Senior Airman"
    strarrCredits(3) = "CFO: Senior Airman"
    strarrCredits(4) = "Board of Directors: Senior Airman"
    strarrCredits(5) = "Lead Designer: Airman Hurdle"
    strarrCredits(6) = "Lead Artist: Airman Hurdle"
    strarrCredits(7) = "Lead Programmer: Airman Hurdle"
    strarrCredits(8) = "Lead Level Designer: Airman Hurdle"
    strarrCredits(9) = "Senior Assistant Designer: Senior Airman"
    strarrCredits(10) = "Senior Hardware Administrator: Airman Jarvis"
    strarrCredits(11) = "Senior Assistant Artist: Airman Hurdle"
    strarrCredits(12) = "Senior Assistant Programmer: Airman Hurdle"
    strarrCredits(13) = "Senior Assistant Level Designer: Airman Hurdle"
    strarrCredits(14) = "Junior Assistant Designer: Airman Basic Parrott"
    strarrCredits(15) = "Junior Assistant Artist: Airman Basic Kollars"
    strarrCredits(16) = "Junior Assistant Programmer: Airman Basic Anderson"
    strarrCredits(17) = "Junior Assistant Level Designer: Airman Basic Kollars"
    strarrCredits(18) = "Junior Code Realigner: Airman Basic Barney"
    strarrCredits(19) = "Software Design Style Consultant: Airman Basic Christen"
    strarrCredits(20) = "Secondary Motivator: Staff Sergeant Drennen"
    strarrCredits(21) = "Best Boy Grip: Airman Basic Zernicke"
    strarrCredits(22) = "Token Retard: Airman Carlson"
    strarrCredits(23) = "Token Cuban A1C: Airman First Class Magby"
    strarrCredits(24) = ""
    strarrCredits(25) = "Special Thanks To Hurdle's Mom"
    
    strarrIcon(1) = "/Icons/CKent.ico"
    strarrIcon(2) = "/Icons/CKent1.ico"
    strarrIcon(3) = "/Icons/CKentIntro.ico"
    strarrIcon(4) = "/Icons/CKent3.ico"
    strarrIcon(5) = "/Icons/GEvil.ico"
    strarrIcon(6) = "/Icons/GEvil1.ico"
    strarrIcon(7) = "/Icons/GEvil2.ico"
    strarrIcon(8) = "/Icons/GEvilIntro.ico"
    strarrIcon(9) = "/Icons/GDeath.ico"
    strarrIcon(10) = "/Icons/SDeath.ico"
    strarrIcon(11) = "/Icons/GPose.ico"
    strarrIcon(12) = "/Icons/GPose2.ico"
    strarrIcon(13) = "/Icons/Spose.ico"
    strarrIcon(14) = "/Icons/SRight2.ico"
    strarrIcon(15) = "/Icons/GDown1.ico"
    strarrIcon(16) = "/Icons/SDownFront.ico"
    strarrIcon(17) = "/Icons/SDownback.ico"
End Sub

Private Sub Image1_Click()
    Unload Me
    Unload frmForm
End Sub

Private Sub Timer1_Timer()
   
    intCredit = (intCredit + 1)
    Update.Caption = strarrCredits(intCredit)

    If intCredit = 25 Then
        intCredit = 0
    End If
End Sub

Private Sub Timer2_Timer()
    Dim intIcon As Integer
    intIcon = ((Rnd * 16) + 1)
    Image1.Picture = LoadPicture(App.Path & strarrIcon(intIcon))
End Sub

