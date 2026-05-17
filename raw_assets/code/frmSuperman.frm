VERSION 5.00
Object = "{22D6F304-B0F6-11D0-94AB-0080C74C7E95}#1.0#0"; "msdxm.ocx"
Begin VB.Form frmForm 
   AutoRedraw      =   -1  'True
   BackColor       =   &H00FFFF00&
   BorderStyle     =   1  'Fixed Single
   Caption         =   "Amazing Adventures of Superman"
   ClientHeight    =   6330
   ClientLeft      =   45
   ClientTop       =   330
   ClientWidth     =   4455
   ForeColor       =   &H00000000&
   Icon            =   "frmSuperman.frx":0000
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   MouseIcon       =   "frmSuperman.frx":030A
   MousePointer    =   2  'Cross
   ScaleHeight     =   6330
   ScaleWidth      =   4455
   StartUpPosition =   2  'CenterScreen
   Begin VB.Timer tmrIntro 
      Interval        =   150
      Left            =   1800
      Top             =   0
   End
   Begin VB.Timer tmrAttack 
      Interval        =   5
      Left            =   1440
      Top             =   0
   End
   Begin VB.Timer tmrGMove 
      Left            =   1080
      Top             =   0
   End
   Begin VB.Timer tmrGCrash 
      Interval        =   100
      Left            =   720
      Top             =   0
   End
   Begin VB.Timer tmrSCrash 
      Interval        =   100
      Left            =   0
      Top             =   0
   End
   Begin VB.Timer tmrSMove 
      Interval        =   30
      Left            =   360
      Top             =   0
   End
   Begin VB.Image imgIntro2 
      Height          =   795
      Left            =   2520
      Picture         =   "frmSuperman.frx":0614
      Stretch         =   -1  'True
      Top             =   120
      Width           =   795
   End
   Begin VB.Image imgIntro1 
      Height          =   795
      Left            =   1320
      Picture         =   "frmSuperman.frx":091E
      Stretch         =   -1  'True
      Top             =   120
      Width           =   795
   End
   Begin VB.Label lblIntro 
      Alignment       =   2  'Center
      BackStyle       =   0  'Transparent
      BorderStyle     =   1  'Fixed Single
      BeginProperty Font 
         Name            =   "Comic Sans MS"
         Size            =   8.25
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H00404040&
      Height          =   5055
      Left            =   720
      TabIndex        =   2
      Top             =   1080
      Width           =   3135
   End
   Begin VB.Image imgG 
      Height          =   795
      Left            =   3000
      Picture         =   "frmSuperman.frx":0C28
      Stretch         =   -1  'True
      Top             =   120
      Width           =   795
   End
   Begin MediaPlayerCtl.MediaPlayer MediaPlayer2 
      Height          =   375
      Left            =   360
      TabIndex        =   1
      Top             =   480
      Visible         =   0   'False
      Width           =   375
      AudioStream     =   -1
      AutoSize        =   0   'False
      AutoStart       =   -1  'True
      AnimationAtStart=   -1  'True
      AllowScan       =   -1  'True
      AllowChangeDisplaySize=   -1  'True
      AutoRewind      =   0   'False
      Balance         =   0
      BaseURL         =   ""
      BufferingTime   =   5
      CaptioningID    =   ""
      ClickToPlay     =   -1  'True
      CursorType      =   0
      CurrentPosition =   -1
      CurrentMarker   =   0
      DefaultFrame    =   ""
      DisplayBackColor=   0
      DisplayForeColor=   16777215
      DisplayMode     =   0
      DisplaySize     =   4
      Enabled         =   -1  'True
      EnableContextMenu=   -1  'True
      EnablePositionControls=   -1  'True
      EnableFullScreenControls=   0   'False
      EnableTracker   =   -1  'True
      Filename        =   ""
      InvokeURLs      =   -1  'True
      Language        =   -1
      Mute            =   0   'False
      PlayCount       =   1
      PreviewMode     =   0   'False
      Rate            =   1
      SAMILang        =   ""
      SAMIStyle       =   ""
      SAMIFileName    =   ""
      SelectionStart  =   -1
      SelectionEnd    =   -1
      SendOpenStateChangeEvents=   -1  'True
      SendWarningEvents=   -1  'True
      SendErrorEvents =   -1  'True
      SendKeyboardEvents=   0   'False
      SendMouseClickEvents=   0   'False
      SendMouseMoveEvents=   0   'False
      SendPlayStateChangeEvents=   -1  'True
      ShowCaptioning  =   0   'False
      ShowControls    =   -1  'True
      ShowAudioControls=   -1  'True
      ShowDisplay     =   0   'False
      ShowGotoBar     =   0   'False
      ShowPositionControls=   -1  'True
      ShowStatusBar   =   0   'False
      ShowTracker     =   -1  'True
      TransparentAtStart=   0   'False
      VideoBorderWidth=   0
      VideoBorderColor=   0
      VideoBorder3D   =   0   'False
      Volume          =   -600
      WindowlessVideo =   0   'False
   End
   Begin MediaPlayerCtl.MediaPlayer MediaPlayer1 
      Height          =   375
      Left            =   0
      TabIndex        =   0
      Top             =   480
      Visible         =   0   'False
      Width           =   375
      AudioStream     =   -1
      AutoSize        =   0   'False
      AutoStart       =   -1  'True
      AnimationAtStart=   -1  'True
      AllowScan       =   -1  'True
      AllowChangeDisplaySize=   -1  'True
      AutoRewind      =   0   'False
      Balance         =   0
      BaseURL         =   ""
      BufferingTime   =   5
      CaptioningID    =   ""
      ClickToPlay     =   -1  'True
      CursorType      =   0
      CurrentPosition =   -1
      CurrentMarker   =   0
      DefaultFrame    =   ""
      DisplayBackColor=   0
      DisplayForeColor=   16777215
      DisplayMode     =   0
      DisplaySize     =   4
      Enabled         =   -1  'True
      EnableContextMenu=   -1  'True
      EnablePositionControls=   -1  'True
      EnableFullScreenControls=   0   'False
      EnableTracker   =   -1  'True
      Filename        =   ""
      InvokeURLs      =   -1  'True
      Language        =   -1
      Mute            =   0   'False
      PlayCount       =   1
      PreviewMode     =   0   'False
      Rate            =   1
      SAMILang        =   ""
      SAMIStyle       =   ""
      SAMIFileName    =   ""
      SelectionStart  =   -1
      SelectionEnd    =   -1
      SendOpenStateChangeEvents=   -1  'True
      SendWarningEvents=   -1  'True
      SendErrorEvents =   -1  'True
      SendKeyboardEvents=   0   'False
      SendMouseClickEvents=   0   'False
      SendMouseMoveEvents=   0   'False
      SendPlayStateChangeEvents=   -1  'True
      ShowCaptioning  =   0   'False
      ShowControls    =   -1  'True
      ShowAudioControls=   -1  'True
      ShowDisplay     =   0   'False
      ShowGotoBar     =   0   'False
      ShowPositionControls=   -1  'True
      ShowStatusBar   =   0   'False
      ShowTracker     =   -1  'True
      TransparentAtStart=   0   'False
      VideoBorderWidth=   0
      VideoBorderColor=   0
      VideoBorder3D   =   0   'False
      Volume          =   -600
      WindowlessVideo =   0   'False
   End
   Begin VB.Image imgS 
      Height          =   795
      Left            =   720
      Picture         =   "frmSuperman.frx":0F32
      Stretch         =   -1  'True
      Top             =   120
      Width           =   795
   End
End
Attribute VB_Name = "frmForm"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

'****Form Values****
Dim blnIntro As Boolean
Dim ndx As Integer
Dim intShotLength As Integer
Dim intFormLeft As Integer
Dim intFormRight As Integer
Dim intCeiling As Integer
Dim intGround As Integer
Dim intInterval As Integer
'****ImageValues****
Dim intImgHeight As Integer
Dim intImgWidth As Integer
'****KeyPress Value Holder****
Dim bytSDir As Byte
Dim intSRndTop As Integer
Dim intSRndLeft As Integer
Dim bytGDir As Byte
Dim intGRndTop As Integer
Dim intGRndLeft As Integer
'****Goblins Move Values****
Dim intGYInc As Integer
Dim intGXInc As Integer
Dim intGY As Integer
Dim intGX As Integer
'****Goblins Attack Values****
Dim intGLineCounter As Integer
Dim intGCounter As Integer
Dim blnGCheck As Boolean
'****Superman Move Values****
Dim intSYInc As Integer
Dim intSXInc As Integer
Dim intSY As Integer
Dim intSX As Integer
'****Superman Attack Values****
Dim intSLineCounter As Integer
Dim intSCounter As Integer
Dim blnSCheck As Boolean
'****Sound Controls****
Dim lngSound As Long
Dim lngAsync As Long
Dim bytSoundtrack As Byte
Dim bytSoundEffect As Byte
'****Speed,Start Point****
Dim intSpeed As Integer
Dim intBaseGroundY As Integer
Dim intBaseCeilingY As Integer
'****ScoreTracker****
Dim intGScore As Integer
Dim intGScoreMod As Integer
Dim intGScoreFin As Integer
Dim intSScore As Integer
Dim intSScoreMod As Integer
Dim intSScoreFin As Integer
Dim intGuyScore As Integer
'****Crash Check****
Dim blnSCrash As Boolean
Dim blnGCrash As Boolean
'****Position Altinators****
Dim bytGPose As Byte
Dim bytSPose As Byte

Private Sub Form_Unload(Cancel As Integer)
    bytSoundtrack = 2
    Call SoundTrack
    frmForm.Hide
    Load Form1
    Form1.Show vbModal
End Sub

Private Sub Form_Load()
    
    
    MediaPlayer2.Volume = -2000
    
    imgS.Enabled = False
    imgG.Enabled = False
    imgS.Visible = False
    imgG.Visible = False
    
    tmrIntro.Enabled = True
    
    tmrSMove.Enabled = False
    tmrGMove.Enabled = False
    tmrGCrash.Enabled = False
    tmrSCrash.Enabled = False

lblIntro.Caption = "Welcome to the best game ever." & vbNewLine & _
        "They aren't bugs, they're features." & vbNewLine & _
        vbNewLine & _
        "Superman's Controls" & vbNewLine & _
        "       UP ARROW   = Up" & vbNewLine & _
        "       DOWN ARROW  = Down" & vbNewLine & _
        "       LEFT ARROW   = Left" & vbNewLine & _
        "       RIGHT ARROW   = Right" & vbNewLine & _
        "       SHIFT   = Shoots" & vbNewLine & _
        "       CONTROL   = Poses" & vbNewLine & _
        "       ENTER   = Restart after death" & vbNewLine & _
        vbNewLine & _
        "Goblin's Controls" & vbNewLine & _
        "       E   = Up" & vbNewLine & _
        "       D   = Down" & vbNewLine & _
        "       S   = Left" & vbNewLine & _
        "       F   = Right" & vbNewLine & _
        "       R   = Shoots" & vbNewLine & _
        "       SPACE   = Poses" & vbNewLine & _
        "       W   = Restart after death" & vbNewLine

    '****Form's StartPoint****
    frmForm.Height = ((2 * Screen.Height) / 3) + 650
    frmForm.Width = Screen.Width / 2
    frmForm.Top = 0
    frmForm.Left = (Screen.Width - Me.ScaleWidth) / 2
    
    '****Create Grass And Clouds****
    FillStyle = vbSolid
    Line (0, frmForm.ScaleHeight - intGround)-Step(Me.ScaleWidth, Me.ScaleHeight), vbGreen, BF
    Line (0, 0)-Step(Me.ScaleWidth, intCeiling), vbWhite, BF

    intShotLength = 350
    arrSLine(0).bytDir = 1
    arrGLine(0).bytDir = 1
    intImgHeight = 850
    intImgWidth = 850

    imgS.Height = intImgHeight
    imgS.Width = intImgWidth
    imgG.Height = intImgHeight
    imgG.Width = intImgWidth
    
    lblIntro.Left = (frmForm.Width - lblIntro.Width) / 2
    imgIntro1.Left = lblIntro.Left
    imgIntro2.Left = lblIntro.Left + lblIntro.Width - imgIntro2.Width
    
    bytSoundEffect = 1
    bytSoundtrack = 2            'Initial Sound
    intSpeed = 500               'Speed Value
    intInterval = 75             'Timer Interval
    
    Call SoundEffect
    Call SoundTrack

End Sub

Public Sub New_Game()
    Randomize
    
    imgS.Enabled = True
    imgG.Enabled = True
    imgS.Visible = True
    imgG.Visible = True
    
    imgIntro1.Enabled = False
    imgIntro2.Enabled = False
    imgIntro1.Visible = False
    imgIntro2.Visible = False
    
    lblIntro.Enabled = False
    lblIntro.Visible = False
    
    tmrIntro.Enabled = False
    
    '****Initial Settings****
    bytGPose = 0                    'Reset Pose
    tmrGCrash.Enabled = False       'Turn Timer Off
    tmrGMove.Enabled = True         'Turn Timer On
    tmrGMove.Interval = intInterval 'Reset Timer
    blnGCrash = False               'Reset Crash Test
    bytGDir = 6                     'Initial Keypress Value
    
    bytSPose = 0                    'Reset Pose
    tmrSCrash.Enabled = False       'Turn Timer Off
    tmrSMove.Enabled = True         'Turn Timer On
    tmrSMove.Interval = intInterval 'Reset Timer
    blnSCrash = False               'Reset Crash Test
    bytSDir = 6                     'Initial Keypress Value
    
    '****Form's StartPoint****
    intGround = 300
    intCeiling = 300
    frmForm.Height = Screen.Height - intGround
    frmForm.Width = 9000
    frmForm.Top = 0
    frmForm.Left = (Screen.Width - Me.ScaleWidth) / 2
    
    '****Set Initial Form Values****
    intBaseGroundY = Me.ScaleHeight - intGround - intImgHeight
    frmForm.Caption = "Goblin Vs. Superman"
    intFormLeft = 0 - intImgWidth / 2
    intFormRight = frmForm.Width - intImgWidth / 2
    
    
    '****Create Grass And Clouds****
    FillStyle = vbSolid
    Line (0, frmForm.ScaleHeight - intGround)-Step(Me.ScaleWidth, Me.ScaleHeight), vbGreen, BF
    Line (0, 0)-Step(Me.ScaleWidth, intCeiling), vbWhite, BF
    
    '****SuperMan's StartPoint****
    intSRndTop = Int((Rnd * (Me.ScaleHeight - intImgHeight - intGround)) + intCeiling)
    imgS.Top = intSRndTop
    intSRndLeft = Int(Rnd * (Me.ScaleWidth - (2 * intImgWidth)) + 1)
    imgS.Left = intSRndLeft
    
    '****Goblin's StartPoint****
    intGRndTop = Int((Rnd * (Me.ScaleHeight - intImgHeight - intGround)) + intCeiling)
    imgG.Top = intGRndTop
    intGRndLeft = Int(Rnd * (Me.ScaleWidth - (2 * intImgWidth)))
    imgG.Left = intGRndLeft
        
    '****Set Initial Locations****
    intSY = imgS.Top
    intSX = imgS.Left

    intGY = imgG.Top
    intGX = imgG.Left
       
    bytSoundtrack = 1
    
   '****Start the game****
    Call SoundTrack
    Call SMove
    Call GMove
End Sub

Private Sub Form_Keydown(KeyCode As Integer, Shift As Integer)

    '****Store Supermans Commands****
    If KeyCode = vbKeyUp Then           'Up
        bytSDir = 1
    ElseIf KeyCode = vbKeyDown Then     'Down
        bytSDir = 2
    ElseIf KeyCode = vbKeyLeft Then     'Left
        bytSDir = 3
    ElseIf KeyCode = vbKeyRight Then    'Right
        bytSDir = 4
    ElseIf KeyCode = vbKeyControl Then  'Pose
        bytSDir = 5
    ElseIf KeyCode = vbKeyShift Then    'Shoot
        If blnSCrash = False Then
            Call SAttack
        End If
    ElseIf KeyCode = vbKeyReturn Then   'Respawn
        If blnSCrash = True Then
            Call SRestart
        End If
    '****Store Goblins Commands****
    ElseIf KeyCode = vbKeyE Then        'Up
        bytGDir = 1
    ElseIf KeyCode = vbKeyD Then        'Down
        bytGDir = 2
    ElseIf KeyCode = vbKeyS Then        'Left
        bytGDir = 3
    ElseIf KeyCode = vbKeyF Then        'Right
        bytGDir = 4
    ElseIf KeyCode = vbKeySpace Then    'Pose
        bytGDir = 5
    ElseIf KeyCode = vbKeyR Then        'Shoot
        If blnGCrash = False Then
            Call GAttack
        End If
    ElseIf KeyCode = vbKeyW Then        'restart
        If blnGCrash = True Then
            Call GRestart
        End If
    '****Store General Commands****
    ElseIf KeyCode = vbKeyF2 Then       'New Game
        Call New_Game
    ElseIf KeyCode = vbKeyDelete Then   'End Program
        Unload frmForm
    End If
    
    '****Call Movement****
    Call GMove
    Call SMove
    
End Sub

Public Sub SMove()

    Select Case bytSDir
        '****Up****
        Case 1
                intSYInc = -intSpeed
                intSXInc = 0
        '****Down****
        Case 2
                If intSY >= (intBaseGroundY) Then
                    intSYInc = 0
                    intSXInc = 0
                    intSY = (intBaseGroundY)
                Else
                    intSYInc = intSpeed
                    intSXInc = 0
                End If
        '****Left****
        Case 3
                intSXInc = -intSpeed
                intSYInc = 0
        '****Right****
        Case 4
                intSXInc = intSpeed
                intSYInc = 0
        '****Pose****
        Case 5
                intSXInc = 0
                intSYInc = 0
        '****Stand****
        Case 6
                intSXInc = 0
                intSYInc = 0
    End Select
End Sub

Public Sub GMove()

    Select Case bytGDir
        '****Up****
        Case 1
                intGYInc = -intSpeed
                intGXInc = 0
        '****Down****
        Case 2
            If intGY >= (intBaseGroundY) Then
                intGYInc = 0
                intGXInc = 0
                intGY = (intBaseGroundY)
            Else
                intGYInc = intSpeed
                intGXInc = 0
            End If
        '****Left****
        Case 3
                intGXInc = -intSpeed
                intGYInc = 0
        '****Right****
        Case 4
                intGXInc = intSpeed
                intGYInc = 0
        '****Pose****
        Case 5
                intGXInc = 0
                intGYInc = 0
        '****Stand****
        Case 6
                intGXInc = 0
                intGYInc = 0
    End Select
End Sub

Public Sub SCrash()

    '****Set The Crash Speed****
    intSYInc = intSpeed
    intSXInc = 0

    '****Rotate the Fall Picture****
    If bytSPose = 0 Then
        imgS.Picture = LoadPicture(App.Path & "\Icons\SSpin1.ico")
        bytSPose = 1
    ElseIf bytSPose = 1 Then
        imgS.Picture = LoadPicture(App.Path & "\Icons\SSpin2.ico")
        bytSPose = 2
    ElseIf bytSPose = 2 Then
        imgS.Picture = LoadPicture(App.Path & "\Icons\SSpin3.ico")
        bytSPose = 3
    Else
        imgS.Picture = LoadPicture(App.Path & "\Icons\SSpin4.ico")
        bytSPose = 0
    End If

End Sub

Public Sub GCrash()

    '****Set The Crash Speed****
    intGYInc = intSpeed
    intGXInc = 0

    '****Rotate the Fall Picture****
    If bytGPose = 0 Then
        imgG.Picture = LoadPicture(App.Path & "\Icons\GSpin1.ico")
        bytGPose = 1
    ElseIf bytGPose = 1 Then
        imgG.Picture = LoadPicture(App.Path & "\Icons\GSpin2.ico")
        bytGPose = 2
    ElseIf bytGPose = 2 Then
        imgG.Picture = LoadPicture(App.Path & "\Icons\GSpin3.ico")
        bytGPose = 3
    Else
        imgG.Picture = LoadPicture(App.Path & "\Icons\GSpin4.ico")
        bytGPose = 0
    End If

End Sub

Public Sub SPose()

    'Check For Ground
    If intSY >= (intBaseGroundY) Then
        intSY = (intBaseGroundY)

        '****Movement On The Ground****
        Select Case bytSDir
            '****Up****
            Case 1
                If bytSPose = 0 Then
                    imgS.Picture = LoadPicture(App.Path & "\Icons\SUp1.ico")
                    bytSPose = 1
                Else
                    imgS.Picture = LoadPicture(App.Path & "\Icons\SUp2.ico")
                    bytSPose = 0
                End If
            '****Down****
            Case 2
                If bytSPose = 0 Then
                    imgS.Picture = LoadPicture(App.Path & "\Icons\CKent3.ico")
                    bytSPose = 1
                Else
                    imgS.Picture = LoadPicture(App.Path & "\Icons\CKent2.ico")
                    bytSPose = 0
                End If
            '****Left****
            Case 3
                If bytSPose = 0 Then
                    imgS.Picture = LoadPicture(App.Path & "\Icons\CKent3.ico")
                    bytSPose = 1
                Else
                    imgS.Picture = LoadPicture(App.Path & "\Icons\CKent2.ico")
                    bytSPose = 0
                End If
            '****Right****
            Case 4
                If bytSPose = 0 Then
                    imgS.Picture = LoadPicture(App.Path & "\Icons\CKent3.ico")
                    bytSPose = 1
                Else
                    imgS.Picture = LoadPicture(App.Path & "\Icons\CKent2.ico")
                    bytSPose = 0
                End If
            '****Pose****
            Case 5
                imgS.Picture = LoadPicture(App.Path & "\Icons\CKent.ico")
            '*****Stand****
            Case 6
                imgS.Picture = LoadPicture(App.Path & "\Icons\CKent1.ico")
        End Select

    '****Movement In The Air****
    Else
        Select Case bytSDir
            '****Up****
            Case 1
                If bytSPose = 0 Then
                    imgS.Picture = LoadPicture(App.Path & "\Icons\SUp1.ico")
                    bytSPose = 1
                Else
                    imgS.Picture = LoadPicture(App.Path & "\Icons\SUp2.ico")
                    bytSPose = 0
                End If
            '****Down****
            Case 2
                If bytSPose = 0 Then
                    imgS.Picture = LoadPicture(App.Path & "\Icons\SDown1.ico")
                    bytSPose = 1
                Else
                    imgS.Picture = LoadPicture(App.Path & "\Icons\SDown2.ico")
                    bytSPose = 0
                End If
            '****Left****
            Case 3
                If bytSPose = 0 Then
                    imgS.Picture = LoadPicture(App.Path & "\Icons\SLeft1.ico")
                    bytSPose = 1
                Else
                    imgS.Picture = LoadPicture(App.Path & "\Icons\SLeft2.ico")
                    bytSPose = 0
                End If
            '****Right****
            Case 4
                If bytSPose = 0 Then
                    imgS.Picture = LoadPicture(App.Path & "\Icons\SRight1.ico")
                    bytSPose = 1
                Else
                    imgS.Picture = LoadPicture(App.Path & "\Icons\SRight2.ico")
                    bytSPose = 0
                End If
            '****Pose****
            Case 5
                imgS.Picture = LoadPicture(App.Path & "\Icons\SPose.ico")
            '****Stand****
            Case 6
                imgS.Picture = LoadPicture(App.Path & "\Icons\SPose.ico")
        End Select
    End If
End Sub

Public Sub GPose()

    'Check For Ground
    If intGY >= (intBaseGroundY) Then
        intGY = (intBaseGroundY)

        '****Movement On The Ground****
        Select Case bytGDir
            '****Up****
            Case 1
                If bytGPose = 0 Then
                    imgG.Picture = LoadPicture(App.Path & "\Icons\GUp1.ico")
                    bytGPose = 1
                Else
                    imgG.Picture = LoadPicture(App.Path & "\Icons\GUp2.ico")
                    bytGPose = 0
                End If
            '****Down****
            Case 2
                If bytGPose = 0 Then
                    imgG.Picture = LoadPicture(App.Path & "\Icons\GEvil2.ico")
                    bytGPose = 1
                Else
                    imgG.Picture = LoadPicture(App.Path & "\Icons\GEvil3.ico")
                    bytGPose = 0
                End If
            '****Left****
            Case 3
                If bytGPose = 0 Then
                    imgG.Picture = LoadPicture(App.Path & "\Icons\GEvil3.ico")
                    bytGPose = 1
                Else
                    imgG.Picture = LoadPicture(App.Path & "\Icons\GEvil2.ico")
                    bytGPose = 0
                End If
            '****Right****
            Case 4
                If bytGPose = 0 Then
                    imgG.Picture = LoadPicture(App.Path & "\Icons\GEvil3.ico")
                    bytGPose = 1
                Else
                    imgG.Picture = LoadPicture(App.Path & "\Icons\GEvil2.ico")
                    bytGPose = 0
                End If
            '****Pose****
            Case 5
                imgG.Picture = LoadPicture(App.Path & "\Icons\GEvil.ico")
            '****Stand****
            Case 6
                imgG.Picture = LoadPicture(App.Path & "\Icons\GEvil1.ico")
        End Select

    '****Movement In The Air****
    Else
        Select Case bytGDir
            '****Up****
            Case 1
                If bytGPose = 0 Then
                    imgG.Picture = LoadPicture(App.Path & "\Icons\GUp1.ico")
                    bytGPose = 1
                Else
                    imgG.Picture = LoadPicture(App.Path & "\Icons\GUp2.ico")
                    bytGPose = 0
                End If
            '****Down****
            Case 2
                If bytGPose = 0 Then
                    imgG.Picture = LoadPicture(App.Path & "\Icons\GDown1.ico")
                    bytGPose = 1
                Else
                    imgG.Picture = LoadPicture(App.Path & "\Icons\GDown2.ico")
                    bytGPose = 0
                End If
            '****Left****
            Case 3
                If bytGPose = 0 Then
                    imgG.Picture = LoadPicture(App.Path & "\Icons\GLeft1.ico")
                    bytGPose = 1
                Else
                    imgG.Picture = LoadPicture(App.Path & "\Icons\GLeft2.ico")
                    bytGPose = 0
                End If
            '****Right****
            Case 4
                If bytGPose = 0 Then
                    imgG.Picture = LoadPicture(App.Path & "\Icons\GRight1.ico")
                    bytGPose = 1
                Else
                    imgG.Picture = LoadPicture(App.Path & "\Icons\GRight2.ico")
                    bytGPose = 0
                End If
            '****Pose****
            Case 5
                imgG.Picture = LoadPicture(App.Path & "\Icons\GPose2.ico")
            '****Pose****
            Case 6
                imgG.Picture = LoadPicture(App.Path & "\Icons\GPose.ico")
        End Select
    End If
End Sub

Private Sub imgG_MouseDown(Button As Integer, Shift As Integer, x As Single, y As Single)
    '****Call Crash Sequence****
        If blnGCrash = False Then
            intGuyScore = intGuyScore + 1
            frmForm.Caption = "Goblin " & intGScoreFin & " Superman " & intSScoreFin & " OmnipotentShootingGuy " & intGuyScore
            bytSoundEffect = 2
            Call SoundEffect
            Call GCrash
            tmrGCrash.Enabled = True
            tmrGMove.Enabled = False
        End If
End Sub

Private Sub imgS_MouseDown(Button As Integer, Shift As Integer, x As Single, y As Single)
    '****Call Crash Sequence****
        If blnSCrash = False Then
            intGuyScore = intGuyScore + 1
            frmForm.Caption = "Goblin " & intGScoreFin & " Superman " & intSScoreFin & " OmnipotentShootingGuy " & intGuyScore
            bytSoundEffect = 2
            Call SoundEffect
            Call SCrash
            tmrSCrash.Enabled = True
            tmrSMove.Enabled = False
        End If
End Sub

Private Sub tmrIntro_Timer()
    
    If blnIntro = True Then
        imgIntro1.Picture = LoadPicture(App.Path & "\Icons\GEvil1.ico")
        imgIntro2.Picture = LoadPicture(App.Path & "\Icons\CKentIntro.ico")
        blnIntro = False
    Else
        imgIntro1.Picture = LoadPicture(App.Path & "\Icons\GEvilIntro.ico")
        imgIntro2.Picture = LoadPicture(App.Path & "\Icons\CKent1.ico")
        blnIntro = True
    End If
End Sub

Private Sub tmrSCrash_Timer()
        If intSY >= (intBaseGroundY) Then
            intSY = (intBaseGroundY)
            intSYInc = 0
            imgS.Top = intSY
            imgS.Picture = LoadPicture(App.Path & "\Icons\SDeath.ico")
            bytSoundEffect = 3
            Call SoundEffect
            tmrSCrash.Enabled = False
        Else
            Call SCrash
        End If
        blnSCrash = True
        intSY = intSY + intSYInc
        imgS.Top = intSY
End Sub

Private Sub tmrGCrash_Timer()
    If intGY >= (intBaseGroundY) Then
        intGY = (intBaseGroundY)
        intGYInc = 0
        imgG.Top = intGY
        imgG.Picture = LoadPicture(App.Path & "\Icons\GDeath.ico")
        bytSoundEffect = 3
        Call SoundEffect
        tmrGCrash.Enabled = False
    Else
        Call GCrash
    End If
    blnGCrash = True
    intGY = intGY + intGYInc
    imgG.Top = intGY
End Sub

Private Sub tmrSMove_Timer()
'****Superman Move Events****
    '****Ground Check****
    If intSY >= (intBaseGroundY) Then
        intSY = (intBaseGroundY)
        If bytSDir <> 1 Then
            intSYInc = 0
        End If
    End If
    
    '****Ceiling Check****
    If imgS.Top <= intCeiling Then
        intSY = intCeiling
        If bytSDir <> 2 Then
            intSYInc = 0
        End If
    End If
    
    '****Score For Posing****
    If bytSDir = 5 Then
        intSScore = intSScore + 1
        intSScoreFin = (intSScore / 10) + intSScoreMod
        frmForm.Caption = "Goblin " & intGScoreFin & " Superman " & intSScoreFin & " OmnipotentShootingGuy " & intGuyScore
    End If
    
    '****Wrap Check****
    If intSX <= intFormLeft Then
        intSX = intFormRight
    ElseIf intSX >= intFormRight Then
        intSX = intFormLeft
    End If
    
    '****Move****
    intSY = intSY + intSYInc
    intSX = intSX + intSXInc
    imgS.Top = intSY
    imgS.Left = intSX

    '****Pose****
    Call SPose
End Sub

Private Sub tmrGMove_Timer()
'****Goblin Move Events****
    '****Ground Check****
    If intGY >= (intBaseGroundY) Then
        intGY = (intBaseGroundY)
        If bytGDir <> 1 Then
            intGYInc = 0
        End If
    End If
    
    '****Ceiling Check****
    If imgG.Top <= intCeiling Then
        imgG.Top = intCeiling
        If bytGDir <> 2 Then
            intGYInc = 0
        End If
    End If

    '****Score For Posing****
    If bytGDir = 5 Then
        intGScore = intGScore + 1
        intGScoreFin = (intGScore / 10) + intGScoreMod
        frmForm.Caption = "Goblin " & intGScoreFin & " Superman " & intSScoreFin & " OmnipotentShootingGuy " & intGuyScore
    End If
    
    '****Wrap Check****
    If intGX <= intFormLeft Then
        intGX = intFormRight
    ElseIf intGX >= intFormRight Then
        intGX = intFormLeft
    End If

    '****Move****
    intGY = intGY + intGYInc
    intGX = intGX + intGXInc
    imgG.Top = intGY
    imgG.Left = intGX

    '****Pose****
    Call GPose

End Sub

Private Sub tmrAttack_Timer()
    DrawSLines
    DrawGLines
End Sub

Private Sub SAttack()
    
    bytSoundEffect = 4
    Call SoundEffect
    
    intSCounter = intSCounter + 1
    With arrSLine(intSCounter)
    Line (.intX, .intY)-(.intNewX, .intNewY), frmForm.BackColor
    .bytLastDir = arrSLine(intSCounter - 1).bytDir
    .bytDir = bytSDir
    .bytWrapCount = 0
    
    .intX = imgS.Left + imgS.Width / 2
    .intY = imgS.Top + imgS.Height / 2
    
NewSDir:
    
    If .bytDir = 1 Then
        .intIncY = -intShotLength
        .intIncX = 0
        .intNewY = .intY + .intIncY
        .intNewX = .intX
        .intBaseY = .intY
    ElseIf .bytDir = 2 Then
        .intIncY = intShotLength
        .intIncX = 0
        .intNewY = .intY + .intIncY
        .intNewX = .intX
        .intBaseY = .intY
    ElseIf .bytDir = 4 Then
        .intIncX = intShotLength
        .intIncY = 0
        .intNewX = .intX + .intIncX
        .intNewY = .intY
        .intBaseX = .intX
    ElseIf .bytDir = 3 Then
        .intIncX = -intShotLength
        .intIncY = 0
        .intNewX = .intX + .intIncX
        .intNewY = .intY
        .intBaseX = .intX
    Else
        .bytDir = .bytLastDir
        GoTo NewSDir
    End If
    
    If intSCounter = 10 Then
        arrSLine(0).bytLastDir = arrSLine(10).bytDir
        intSCounter = 1
        intSLineCounter = 10
        blnSCheck = True
    ElseIf blnSCheck = False Then
        intSLineCounter = intSCounter
    End If
    
    Line (.intX, .intY)-(.intNewX, .intNewY), vbRed
    End With
End Sub

Private Sub DrawSLines()

    For ndx = 1 To intSLineCounter
        With arrSLine(ndx)
            Line (.intX, .intY)-(.intNewX, .intNewY), frmForm.BackColor
            .intX = .intX + .intIncX
            .intY = .intY + .intIncY
            .intNewX = .intNewX + .intIncX
            .intNewY = .intNewY + .intIncY
            Line (.intX, .intY)-(.intNewX, .intNewY), vbRed
            Call SHit
            Call SWrap
        End With
    Next
End Sub

Public Sub SWrap()
    '****Up and Down****
    With arrSLine(ndx)
    If .bytDir = 1 Then
            If .intNewY <= intCeiling Then
                 Line (.intX, .intY)-(.intNewX, .intNewY), frmForm.BackColor
                .intNewY = intCeiling
                .intY = .intNewY + .intIncY
                .intIncY = 0
                FillStyle = vbSolid
                Line (0, 0)-Step(Me.ScaleWidth, intCeiling), vbWhite, BF
            End If
    ElseIf .bytDir = 2 Then
            If .intY >= (intBaseGroundY + intImgHeight) Then
                Line (.intX, .intY)-(.intNewX, .intNewY), frmForm.BackColor
                .intNewY = (Me.ScaleHeight + intImgHeight)
                .intY = .intNewY - .intIncY
                .intIncY = 0
                Line (.intX, .intY)-(.intNewX, .intNewY), frmForm.BackColor
                FillStyle = vbSolid
                Line (0, frmForm.ScaleHeight - intGround)-Step(Me.ScaleWidth, Me.ScaleHeight), vbGreen, BF
            End If
    '****Left and Right****
    ElseIf .intNewX <= intFormLeft Then
        Line (.intX, .intY)-(.intNewX, .intNewY), frmForm.BackColor
        .intNewX = intFormRight - 1
        .intX = intFormRight + .intIncX
        Call SWrapCheck
        .bytWrapCount = .bytWrapCount + 1
    ElseIf arrSLine(ndx).intNewX >= intFormRight Then
        Line (.intX, .intY)-(.intNewX, .intNewY), frmForm.BackColor
        .intNewX = intFormLeft + 1
        .intX = intFormLeft - .intIncX
        Call SWrapCheck
        .bytWrapCount = .bytWrapCount + 1
    End If
    End With
End Sub

Public Sub SHit()
    With arrSLine(ndx)
    If .bytDir = 1 Or .bytDir = 2 Then
        If ((.intNewY >= imgG.Top) And (.intNewY <= (imgG.Top + imgG.Height))) Or ((.intY >= imgG.Top) And (.intY <= (imgG.Top + imgG.Height))) Then
            If .intNewX >= imgG.Left And .intNewX <= (imgG.Left + imgG.Width) Then
                 Line (.intX, .intY)-(.intNewX, .intNewY), frmForm.BackColor
                .intNewY = 0
                .intY = 0
                .intIncY = 0
                .intNewX = 0
                .intX = 0
                .intIncX = 0
                
                If blnGCrash = False Then
                    intSScoreMod = intSScoreMod + 10
                    intSScoreFin = (intSScore / 10) + intSScoreMod
                    frmForm.Caption = "Goblin " & intGScoreFin & " Superman " & intSScoreFin & " OmnipotentShootingGuy " & intGuyScore
                    bytSoundEffect = 2
                    Call SoundEffect
                    Call GCrash
                    blnGCrash = True
                    tmrGCrash.Enabled = True
                    tmrGMove.Enabled = False
                End If
            End If
        End If
    ElseIf .bytDir = 3 Or 4 Then
        If ((.intNewX >= imgG.Left) And (.intNewX <= (imgG.Left + imgG.Width))) Or ((.intX >= imgG.Left) And (.intX <= (imgG.Left + imgG.Width))) Then
            If .intNewY >= imgG.Top And .intNewY <= (imgG.Top + imgG.Height) Then
                 Line (.intX, .intY)-(.intNewX, .intNewY), frmForm.BackColor
                .intNewY = 0
                .intY = 0
                .intIncY = 0
                .intNewX = 0
                .intX = 0
                .intIncX = 0
                
                If blnGCrash = False Then
                    intSScoreMod = intSScoreMod + 10
                    intSScoreFin = (intSScore / 10) + intSScoreMod
                    frmForm.Caption = "Goblin " & intGScoreFin & " Superman " & intSScoreFin & " OmnipotentShootingGuy " & intGuyScore
                    bytSoundEffect = 2
                    Call SoundEffect
                    Call GCrash
                    blnGCrash = True
                    tmrGCrash.Enabled = True
                    tmrGMove.Enabled = False
                End If
            End If
        End If
    End If
    End With
End Sub

Public Sub SWrapCheck()
    With arrSLine(ndx)
        If .bytWrapCount = 2 Then
            Line (.intX, .intY)-(.intNewX, .intNewY), frmForm.BackColor
                .intNewY = 0
                .intY = 0
                .intIncY = 0
                .intNewX = 0
                .intX = 0
                .intIncX = 0
        End If
    End With
End Sub

Private Sub GAttack()
    
    bytSoundEffect = 4
    Call SoundEffect
    
    intGCounter = intGCounter + 1
    With arrGLine(intGCounter)
    Line (.intX, .intY)-(.intNewX, .intNewY), frmForm.BackColor
   .bytLastDir = arrGLine(intGCounter - 1).bytDir
   .bytDir = bytGDir
   .bytWrapCount = 0
    
    .intX = imgG.Left + imgS.Width / 2
    .intY = imgG.Top + imgS.Height / 2
    
NewSDir:
    
    If .bytDir = 1 Then
        .intIncY = -intShotLength
        .intIncX = 0
        .intNewY = .intY + .intIncY
        .intNewX = .intX
        .intBaseY = .intY
    ElseIf .bytDir = 2 Then
        .intIncY = intShotLength
        .intIncX = 0
        .intNewY = .intY + .intIncY
        .intNewX = .intX
        .intBaseY = .intY
    ElseIf .bytDir = 4 Then
        .intIncX = intShotLength
        .intIncY = 0
        .intNewX = .intX + .intIncX
        .intNewY = .intY
        .intBaseX = .intX
    ElseIf .bytDir = 3 Then
        .intIncX = -intShotLength
        .intIncY = 0
        .intNewX = .intX + .intIncX
        .intNewY = .intY
        .intBaseX = .intX
    Else
        .bytDir = .bytLastDir
        GoTo NewSDir
    End If
    
    If intGCounter = 10 Then
        arrGLine(0).bytLastDir = arrGLine(10).bytDir
        intGCounter = 1
        intGLineCounter = 10
        blnGCheck = True
    ElseIf blnGCheck = False Then
        intGLineCounter = intGCounter
    End If
    
    Line (.intX, .intY)-(.intNewX, .intNewY), &H80FF&
    End With
End Sub

Private Sub DrawGLines()

    For ndx = 1 To intGLineCounter
        With arrGLine(ndx)
            Line (.intX, .intY)-(.intNewX, .intNewY), frmForm.BackColor
            .intX = .intX + .intIncX
            .intY = .intY + .intIncY
            .intNewX = .intNewX + .intIncX
            .intNewY = .intNewY + .intIncY
            Line (.intX, .intY)-(.intNewX, .intNewY), &H80FF&
            Call GHit
            Call GWrap
        End With
    Next
End Sub

Public Sub GWrap()
    '****Up and Down****
    With arrGLine(ndx)
    If .bytDir = 1 Then
            If .intNewY <= intCeiling Then
                 Line (.intX, .intY)-(.intNewX, .intNewY), frmForm.BackColor
                .intNewY = intCeiling
                .intY = .intNewY + .intIncY
                .intIncY = 0
                FillStyle = vbSolid
                Line (0, 0)-Step(Me.ScaleWidth, intCeiling), vbWhite, BF
            End If
    ElseIf .bytDir = 2 Then
            If .intY >= (intBaseGroundY + intImgHeight) Then
                Line (.intX, .intY)-(.intNewX, .intNewY), frmForm.BackColor
                .intNewY = (Me.ScaleHeight + intImgHeight)
                .intY = .intNewY - .intIncY
                .intIncY = 0
                Line (.intX, .intY)-(.intNewX, .intNewY), frmForm.BackColor
                FillStyle = vbSolid
                Line (0, frmForm.ScaleHeight - intGround)-Step(Me.ScaleWidth, Me.ScaleHeight), vbGreen, BF
            End If
    '****Left and Right****
    ElseIf .intNewX < intFormLeft Then
        Line (.intX, .intY)-(.intNewX, .intNewY), frmForm.BackColor
        .intNewX = intFormRight
        .intX = intFormRight + .intIncX
        Call GWrapCheck
        .bytWrapCount = .bytWrapCount + 1
    ElseIf .intNewX > intFormRight + .intIncX Then
        Line (.intX, .intY)-(.intNewX, .intNewY), frmForm.BackColor
        .intNewX = intFormLeft
        .intX = intFormLeft - .intIncX
        Call GWrapCheck
        .bytWrapCount = .bytWrapCount + 1
    End If
    End With
End Sub

Public Sub GWrapCheck()
    With arrGLine(ndx)
        If .bytWrapCount = 2 Then
            Line (.intX, .intY)-(.intNewX, .intNewY), frmForm.BackColor
                .intNewY = 0
                .intY = 0
                .intIncY = 0
                .intNewX = 0
                .intX = 0
                .intIncX = 0
        End If
    End With
End Sub

Public Sub GHit()
    With arrGLine(ndx)
    If .bytDir = 1 Or .bytDir = 2 Then
        If ((.intNewY >= imgS.Top) And (.intNewY <= (imgS.Top + imgS.Height))) Or ((.intY >= imgS.Top) And (.intY <= (imgG.Top + imgS.Height))) Then
            If .intNewX >= imgS.Left And .intNewX <= (imgS.Left + imgS.Width) Then
                 Line (.intX, .intY)-(.intNewX, .intNewY), frmForm.BackColor
                .intNewY = 0
                .intY = 0
                .intIncY = 0
                .intNewX = 0
                .intX = 0
                .intIncX = 0
                
                If blnSCrash = False Then
                    intGScoreMod = intGScoreMod + 10
                    intGScoreFin = (intGScore / 10) + intGScoreMod
                    frmForm.Caption = "Goblin " & intGScoreFin & " Superman " & intSScoreFin & " OmnipotentShootingGuy " & intGuyScore
                    bytSoundEffect = 2
                    blnSCrash = True
                    Call SoundEffect
                    Call SCrash
                    tmrSCrash.Enabled = True
                    tmrSMove.Enabled = False
                End If
            End If
        End If
    ElseIf .bytDir = 3 Or 4 Then
        If ((.intNewX >= imgS.Left) And (.intNewX <= (imgS.Left + imgS.Width))) Or ((.intX >= imgS.Left) And (.intX <= (imgS.Left + imgS.Width))) Then
            If .intNewY >= imgS.Top And .intNewY <= (imgS.Top + imgS.Height) Then
                 Line (.intX, .intY)-(.intNewX, .intNewY), frmForm.BackColor
                .intNewY = 0
                .intY = 0
                .intIncY = 0
                .intNewX = 0
                .intX = 0
                .intIncX = 0
                
                If blnSCrash = False Then
                    intGScoreMod = intGScoreMod + 10
                    intGScoreFin = (intGScore / 10) + intGScoreMod
                    frmForm.Caption = "Goblin " & intGScoreFin & " Superman " & intSScoreFin & " OmnipotentShootingGuy " & intGuyScore
                    bytSoundEffect = 2
                    blnSCrash = True
                    Call SoundEffect
                    Call SCrash
                    tmrSCrash.Enabled = True
                    tmrSMove.Enabled = False
                End If
            End If
        End If
    End If
    End With
End Sub

Public Sub SRestart()
    Randomize
    
    '****Initial Settings****
    bytSPose = 0                    'Reset Pose
    tmrSCrash.Enabled = False       'Turn Timer Off
    tmrSMove.Enabled = True         'Turn Timer On
    tmrSMove.Interval = intInterval 'Reset Timer
    blnSCrash = False               'Reset Crash Test
    bytSDir = 6                     'Initial Keypress Value

    '****SuperMan's StartPoint****
    intSRndTop = Int((Rnd * (Me.ScaleHeight - intImgHeight - intGround)) + intCeiling)
    imgS.Top = intSRndTop
    intSRndLeft = Int(Rnd * (Me.ScaleWidth - (2 * intImgWidth)) + 1)
    imgS.Left = intSRndLeft

    '****Set Initial Locations****
    intSY = imgS.Top
    intSX = imgS.Left
End Sub

Public Sub GRestart()
    Randomize
    
    '****Initial Settings****
    bytGPose = 0                    'Reset Pose
    tmrGCrash.Enabled = False       'Turn Timer Off
    tmrGMove.Enabled = True         'Turn Timer On
    tmrGMove.Interval = intInterval 'Reset Timer
    blnGCrash = False               'Reset Crash Test
    bytGDir = 6                     'Initial Keypress Value

    '****Goblin's StartPoint****
    intGRndTop = Int((Rnd * (Me.ScaleHeight - intImgHeight - intGround)) + intCeiling)
    imgG.Top = intGRndTop
    intGRndLeft = Int(Rnd * (Me.ScaleWidth - (2 * intImgWidth)))
    imgG.Left = intGRndLeft
    
    '****Set Initial Locations****
    intGY = imgG.Top
    intGX = imgG.Left
    
End Sub

Public Sub SoundEffect()
    '****Sound Effect Selector****
    Select Case bytSoundEffect
    Case 1
        MediaPlayer1.FileName = App.Path & "\Sounds\Intro.wav"
    Case 2
        MediaPlayer1.FileName = App.Path & "\Sounds\DeathCry.wav"
    Case 3
        MediaPlayer1.FileName = App.Path & "\Sounds\Explode.wav"
    Case 4
        MediaPlayer1.FileName = App.Path & "\Sounds\Laser.wav"
    End Select
    MediaPlayer1.Play
End Sub

Public Sub SoundTrack()
    '****Sound Track Selector****
    Select Case bytSoundtrack
    Case 1
        MediaPlayer2.FileName = App.Path & "\Sounds\Passport.mid"
    Case 2
        MediaPlayer2.FileName = App.Path & "\Sounds\Canyon.mid"
    End Select
    MediaPlayer2.Play
End Sub


