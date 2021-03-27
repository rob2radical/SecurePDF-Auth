import sys


#int hash(char szKey[],int iMaxHash)
#{
#    int iHash = 0;
#    int i;
#    if (iMaxHash <= 0)
#        errExit("hash function received an invalid iMaxHash value: %d\n"
#            , iMaxHash);
#    for (i = 0; i < (int) strlen(szKey); i++)
#    {
#        iHash += szKey[i];
#    }
#    // restrict it to the hash area
#    iHash = abs(iHash) % iMaxHash +1;
#    return iHash;
#}